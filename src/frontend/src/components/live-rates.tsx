import { LabelData, NotificationType, state } from '@/library/api';
import { Reference } from '@/library/context';
import { formatAddressName, formatDimension, formatFullAddress, formatRef, formatWeight } from '@/library/helper';
import { Collection } from '@/library/types';
import { ErrorResponse, Payment, Rate, Shipment } from '@purplship/purplship';
import { useNavigate } from '@reach/router';
import React, { useState } from 'react';
import ButtonField from './generic/button-field';

interface LiveRatesComponent {
    shipment: Shipment;
    update: (payload: {}) => void;
}

const LiveRates: React.FC<LiveRatesComponent> = ({ shipment, update }) => {
    const [lastState, setLastSate] = useState<Shipment | undefined>(undefined);
    const [countries, setCountries] = useState<Collection | undefined>(undefined);
    const [loading, setLoading] = useState<boolean>(false);
    const [selected_rate, setSelectedRate] = useState<string | undefined>();
    const navigate = useNavigate();
    const computeEnable = (shipment: Shipment) => {
        return (
            shipment.recipient.address_line1 === undefined ||
            shipment.shipper.address_line1 === undefined ||
            shipment.parcels.length === 0 ||
            lastState == shipment
        );
    };
    const fetchRates = async () => {
        let rates: Rate[] | undefined = undefined;
        try {
            setLoading(true);
            setLastSate(shipment);
            const response = await state.fetchShipmentRates(shipment);
            rates = response.rates;
        } catch (err) {
            let message = err.message
            if (err.response?.error !== undefined) {
                message = ((err.response.error.details as ErrorResponse).messages || []).map(msg => (
                    <p>{msg.carrier_name}: {msg.message}</p>
                ))
            }
            state.setNotification({ type: NotificationType.error, message });
        } finally {
            setLoading(false);
            setSelectedRate(undefined);
            update({ rates, selected_rate_id: undefined });
        }
    };
    const buyShipment = async () => {
        try {
            setLoading(true);
            let currency = (shipment.options || {}).currency || Payment.CurrencyEnum.CAD;
            const response = await state.buyShipmentLabel({
                ...shipment,
                rates: shipment.rates as Rate[],
                selected_rate_id: selected_rate as string,
                payment: { paid_by: Payment.PaidByEnum.Sender, currency } as Payment
            });
            update(response.shipment as Shipment);
            state.setNotification({ type: NotificationType.success, message: 'Label successfully purchased!' });
            navigate('/');
        } catch (err) {
            let message = err.message
            if (err.response?.error !== undefined) {
                message = ((err.response.error.details as ErrorResponse).messages || []).map(msg => (
                    <p>{msg.carrier_name}: {msg.message}</p>
                ))
            }
            state.setNotification({ type: NotificationType.error, message });
        } finally {
            setLoading(false);
        }
    };

    return (
        <div>
            <div className="columns is-multiline">

                <Reference.Consumer>
                    {(ref) => {
                        if (Object.values(ref || {}).length > 0) setCountries(ref.countries as {})
                        return <></>;
                    }}
                </Reference.Consumer>

                <div className="column is-12 pb-2">
                    <span className="title is-5">Shipment Details</span>

                    <button className={`button is-small is-outlined is-info is-pulled-right ${loading ? 'is-loading' : ''}`} onClick={fetchRates} disabled={computeEnable(shipment)}>
                        <span>Fetch Rates</span>
                    </button>
                </div>

                <div className="column is-12 py-1" style={shipment.shipper.address_line1 === undefined ? { display: 'none' } : {}}>

                    <p className="is-title is-size-6 my-2 has-text-weight-semibold">Shipper Address</p>
                    <p className="is-subtitle is-size-7 my-1 has-text-weight-semibold">{formatAddressName(shipment.shipper)}</p>
                    <p className="is-subtitle is-size-7 my-1 has-text-weight-semibold has-text-grey">{formatFullAddress(shipment.shipper, countries)}</p>

                </div>

                <div className="column is-12 py-1" style={{ display: `${shipment.recipient.address_line1 === undefined ? 'none' : 'block'}` }}>

                    <p className="is-title is-size-6 my-2 has-text-weight-semibold">Recipient Address</p>
                    <p className="is-subtitle is-size-7 my-1 has-text-weight-semibold">{formatAddressName(shipment.recipient)}</p>
                    <p className="is-subtitle is-size-7 my-1 has-text-weight-semibold has-text-grey">{formatFullAddress(shipment.recipient, countries)}</p>

                </div>

                <div className="column is-12 py-1" style={{ display: `${shipment.parcels.length == 0 ? 'none' : 'block'}` }}>

                    <p className="is-title is-size-6 my-2 has-text-weight-semibold">Parcel</p>
                    <p className="is-subtitle is-size-7 my-1 has-text-weight-semibold has-text-grey">{formatDimension(shipment.parcels[0])}</p>
                    <p className="is-subtitle is-size-7 my-1 has-text-weight-semibold has-text-grey">{formatWeight(shipment.parcels[0])}</p>

                </div>

                <div className="column is-12 py-3" style={{ display: `${shipment.rates === undefined ? 'none' : 'block'}` }}>

                    <h6 className="is-title is-size-6 mt-1 mb-4 has-text-weight-semibold">Live Rates</h6>

                    <ul className="menu-list">
                        {shipment.rates?.map(rate => (
                            <li key={rate.id}>
                                <a className={`columns mb-0 ${rate.id === selected_rate ? 'has-text-grey-dark' : 'has-text-grey'}`} onClick={() => setSelectedRate(rate.id)}>

                                    <span className={`icon is-medium ${rate.id === selected_rate ? 'has-text-success' : ''}`}>
                                        {(rate.id === selected_rate) ? <i className="fas fa-check-square"></i> : <i className="fas fa-square"></i>}
                                    </span>

                                    <div className="is-size-7 has-text-weight-semibold">
                                        <h6 className="has-text-weight-bold">{formatRef(rate.service as string)}</h6>
                                        <span>{rate.total_charge} {rate.currency}</span>
                                        {(rate.transit_days !== null) && <span> - {rate.transit_days} Transit days</span>}
                                    </div>
                                </a>
                            </li>
                        ))}
                    </ul>

                </div>

            </div>

            <ButtonField
                onClick={buyShipment}
                fieldClass="has-text-centered mt-3"
                className={`is-success ${loading ? 'is-loading' : ''}`}
                style={shipment.rates === undefined ? { display: 'none' } : {}}
                disabled={selected_rate === undefined}>
                <span>Buy</span>
            </ButtonField>

        </div>
    )
};

export default LiveRates;
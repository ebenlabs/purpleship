import unittest
from unittest.mock import patch, ANY
from tests.chronopost.fixture import gateway

import karrio
import karrio.lib as lib
import karrio.core.models as models


class TestChronopostShipping(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.ShipmentRequest = models.ShipmentRequest(**ShipmentPayload)
        self.ShipmentCancelRequest = models.ShipmentCancelRequest(
            **ShipmentCancelPayload
        )

    def test_create_shipment_request(self):
        request = gateway.mapper.create_shipment_request(self.ShipmentRequest)

        self.assertEqual(request.serialize(), ShipmentRequest)

    def test_create_cancel_shipment_request(self):
        request = gateway.mapper.create_cancel_shipment_request(
            self.ShipmentCancelRequest
        )
        self.assertEqual(request.serialize(), ShipmentCancelRequest)

    def test_create_shipment(self):
        with patch("karrio.mappers.chronopost.proxy.lib.request") as mock:
            mock.return_value = "<a></a>"
            karrio.Shipment.create(self.ShipmentRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}/shipping-cxf/ShippingServiceWS",
            )

    def test_cancel_shipment(self):
        with patch("karrio.mappers.chronopost.proxy.lib.request") as mock:
            mock.return_value = "<a></a>"
            karrio.Shipment.cancel(self.ShipmentCancelRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}/tracking-cxf/TrackingServiceWS",
            )

    def test_parse_shipment_response(self):
        with patch("karrio.mappers.chronopost.proxy.lib.request") as mock:
            mock.return_value = ShipmentResponse
            parsed_response = (
                karrio.Shipment.create(self.ShipmentRequest).from_(gateway).parse()
            )
            self.assertListEqual(lib.to_dict(parsed_response), ParsedShipmentResponse)

    def test_parse_cancel_shipment_error_response(self):
        with patch("karrio.mappers.chronopost.proxy.lib.request") as mock:
            mock.return_value = ""
            parsed_response = (
                karrio.Shipment.cancel(self.ShipmentCancelRequest)
                .from_(gateway)
                .parse()
            )
            print(lib.to_dict(parsed_response))
            self.assertListEqual(
                lib.to_dict(parsed_response), ParsedCancelShipmentResponse
            )


if __name__ == "__main__":
    unittest.main()


ShipmentPayload = {
    "service": "chronopost_13",
    "shipper": {
        "company_name": "Chef Royale",
        "person_name": "Jean Dupont",
        "address_line1": "28 rue du Clair Bocage",
        "city": "La Seyne-sur-mer",
        "postal_code": "83500",
        "country_code": "FR",
        "phone_number": "+330447110494",
    },
    "recipient": {
        "company_name": "HautSide",
        "person_name": "Lucas Dupont",
        "address_line1": "72 rue Reine Elisabeth",
        "city": "Menton",
        "postal_code": "06500",
        "country_code": "FR",
    },
    "parcels": [
        {
            "height": 15,
            "length": 60.0,
            "width": 30,
            "weight": 5.0,
            "weight_unit": "KG",
            "dimension_unit": "CM",
        }
    ],
    "label_type": "PDF",
    "reference": "Ref. 123456",
    "options": {"shipment_date": "2022-08-16T22:56:11"},
}

ShipmentCancelPayload = {
    "shipment_identifier": "794947717776",
}

ParsedShipmentResponse = [
    {
        "carrier_id": "chronopost",
        "carrier_name": "chronopost",
        "docs": {},
        "meta": {},
    },
    [],
]

ParsedCancelShipmentResponse = [
    None,
    [
        {
            "carrier_id": "chronopost",
            "carrier_name": "chronopost",
            "code": 4,
            "message": "Document is empty, line 1, column 1 (<string>, line 1)",
        }
    ],
]


ShipmentRequest = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:cxf="http://cxf.shipping.soap.chronopost.fr/">
    <soapenv:Body>
        <soapenv:shippingMultiParcelV5>
            <headerValue>
                <accountNumber>1234</accountNumber>
                <idEmit>CHRFR</idEmit>
            </headerValue>
            <shipperValue>
                <shipperAdress1>28 rue du Clair Bocage</shipperAdress1>
                <shipperAdress2></shipperAdress2>
                <shipperCity>La Seyne-sur-mer</shipperCity>
                <shipperCivility>M</shipperCivility>
                <shipperContactName>Jean Dupont</shipperContactName>
                <shipperCountry>FR</shipperCountry>
                <shipperCountryName>France</shipperCountryName>
                <shipperMobilePhone>+330447110494</shipperMobilePhone>
                <shipperName>Chef Royale</shipperName>
                <shipperName2>Chef Royale</shipperName2>
                <shipperPreAlert>0</shipperPreAlert>
                <shipperZipCode>83500</shipperZipCode>
            </shipperValue>
            <customerValue>
                <customerAdress1>72 rue Reine Elisabeth</customerAdress1>
                <customerAdress2></customerAdress2>
                <customerCity>Menton</customerCity>
                <customerContactName>Lucas Dupont</customerContactName>
                <customerCountry>FR</customerCountry>
                <customerCountryName>France</customerCountryName>
                <customerName>HautSide</customerName>
                <customerName2>HautSide</customerName2>
                <customerPreAlert>0</customerPreAlert>
                <customerZipCode>06500</customerZipCode>
            </customerValue>
            <recipientValue>
                <recipientAdress1>72 rue Reine Elisabeth</recipientAdress1>
                <recipientAdress2></recipientAdress2>
                <recipientCity>Menton</recipientCity>
                <recipientContactName>Lucas Dupont</recipientContactName>
                <recipientCountry>FR</recipientCountry>
                <recipientCountryName>France</recipientCountryName>
                <recipientName>HautSide</recipientName>
                <recipientName2>HautSide</recipientName2>
                <recipientPreAlert>0</recipientPreAlert>
                <recipientZipCode>06500</recipientZipCode>
            </recipientValue>
            <refValue>
                <shipperRef>Ref. 123456</shipperRef>
            </refValue>
            <skybillValue>
                <bulkNumber>1</bulkNumber>
                <evtCode>DC</evtCode>
                <objectType>MAR</objectType>
                <productCode>01</productCode>
                <service>0</service>
                <shipDate>2022-08-16T22:56:11</shipDate>
                <shipHour>22</shipHour>
                <weight>5.</weight>
                <weightUnit>KGM</weightUnit>
            </skybillValue>
            <skybillParamsValue>
                <mode>PDF</mode>
            </skybillParamsValue>
            <password>password</password>
            <modeRetour>1</modeRetour>
            <numberOfParcel>1</numberOfParcel>
            <version>2.0</version>
            <multiParcel>N</multiParcel>
        </soapenv:shippingMultiParcelV5>
    </soapenv:Body>
</soapenv:Envelope>
"""

ShipmentCancelRequest = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:cxf="http://cxf.tracking.soap.chronopost.fr/">
    <soapenv:Body>
        <soapenv:cancelSkybill>
            <accountNumber>1234</accountNumber>
            <password>password</password>
            <language>en_GB</language>
            <skybillNumber>794947717776</skybillNumber>
        </soapenv:cancelSkybill>
    </soapenv:Body>
</soapenv:Envelope>
"""

ShipmentResponse = """<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
    <soap:Body>
        <ns1:shippingMultiParcelV5Response xmlns:ns1="http://cxf.shipping.soap.chronopost.fr/">
            <return>
                <errorCode>0</errorCode>
                <errorMessage />
                <resultMultiParcelValue>
                    <codeDepot>75327227</codeDepot>
                    <codeService>226</codeService>
                    <destinationDepot>0477</destinationDepot>
                    <geoPostCodeBarre>%0006500XP696982485248226250</geoPostCodeBarre>
                    <geoPostNumeroColis>XP696982485248D</geoPostNumeroColis>
                    <groupingPriorityLabel>SIA1</groupingPriorityLabel>
                    <pdfetiquette>iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAIAAACQd1PeAAAADElEQVR4XmOYyfAfAALOAZlbSAeZAAAAAElFTkSuQmCC</pdfetiquette>
                    <serviceMark />
                    <serviceName>AM2-NO</serviceName>
                    <signaletiqueProduit>13H</signaletiqueProduit>
                    <skybillNumber>XP696982485FR</skybillNumber>
                </resultMultiParcelValue>
            </return>
        </ns1:shippingMultiParcelV5Response>
    </soap:Body>
</soap:Envelope>
"""
ShipmentCancelErrorResponse = """<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
    <soap:Body>
        <ns2:cancelSkybillResponse xmlns:ns2="http://cxf.tracking.soap.chronopost.fr/">
            <return>
                <errorCode>2</errorCode>
                <errorMessage>the parcel doesn't match account or parcel information not found</errorMessage>
                <statusCode>0</statusCode>
            </return>
        </ns2:cancelSkybillResponse>
    </soap:Body>
</soap:Envelope>
"""

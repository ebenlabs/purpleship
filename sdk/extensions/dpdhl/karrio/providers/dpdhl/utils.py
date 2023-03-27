import base64
import karrio.lib as lib
import karrio.core as core
import dpdhl_lib.business_interface as dpdhl

AuthentificationType = lib.mutate_xml_object_type(
    dpdhl.AuthentificationType,
    tag_name="Authentification",
)


class Settings(core.Settings):
    """Deutsche Post DHL connection settings."""

    # required carrier specific properties
    username: str  # type:ignore
    password: str  # type:ignore
    app_id: str = None
    app_token: str = None
    zt_id: str = None
    zt_password: str = None
    account_number: str = None
    language_code: str = "en"

    @property
    def carrier_name(self):
        return "dpdhl"

    @property
    def server_url(self):
        return (
            "https://cig.dhl.de/services/sandbox"
            if self.test_mode
            else "https://cig.dhl.de/services/production"
        )

    @property
    def basic_authentication(self):
        pair = "%s:%s" % (
            (self.username, self.password)
            if self.test_mode else
            (self.app_id, self.app_token)
        )
        return base64.b64encode(pair.encode("utf-8")).decode("ascii")

    @property
    def tracking_url(self):
        return "https://www.dhl.de/" + self.language_code + "/privatkunden/pakete-empfangen/verfolgen.html?piececode={}"

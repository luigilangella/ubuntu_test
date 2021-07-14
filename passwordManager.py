import secretManager

# ----------------------------------------------GIS ACCOUNT---------------------------------------------------- #
u = secretManager.access_secret_version('kier-nonprod','GIS_USER','latest')
p = secretManager.access_secret_version('kier-nonprod','GIS-PWD','latest')

# ----------------------------------------------EMAIL ACCOUNT---------------------------------------------------- #
ProveitEmail = secretManager.access_secret_version('kier-nonprod','ProveitEmail','latest')
ProveitPassword = secretManager.access_secret_version('kier-nonprod','ProveitPassword','latest')

# ----------------------------------------------AZURE ACCOUNT---------------------------------------------------- #
account_key = secretManager.access_secret_version('kier-nonprod','azure_account_key','latest')
connection_string = secretManager.access_secret_version('kier-nonprod','azure_connection_string','latest')

# ----------------------------------------------POSTGRES ACCOUNT---------------------------------------------------- #
DB_USER = secretManager.access_secret_version('kier-nonprod','DB_USER','latest')
DB_P = secretManager.access_secret_version('kier-nonprod','DB_P','latest')
DB_HOST = secretManager.access_secret_version('kier-nonprod','DB_HOST','latest')
DB_PORT = secretManager.access_secret_version('kier-nonprod','DB_PORT','latest')
DB_NAME = secretManager.access_secret_version('kier-nonprod','DB_NAME','latest')

# ----------------------------------------------BT ACCOUNT---------------------------------------------------- #
BT_Searcher_user = secretManager.access_secret_version('kier-nonprod','BT_Searcher_user','latest')
BT_Searcher_passW = secretManager.access_secret_version('kier-nonprod','BT_Searcher_passW','latest')
BT_username = secretManager.access_secret_version('kier-nonprod','BT_username','latest')
BT_password = secretManager.access_secret_version('kier-nonprod','BT_password','latest')

# ----------------------------------------------CITYFIBER ACCOUNT---------------------------------------------------- #
CityFiberUsername = secretManager.access_secret_version('kier-nonprod','CityFiberUsername','latest')
CityFiberPassword = secretManager.access_secret_version('kier-nonprod','CityFiberPassword','latest')

# ----------------------------------------------USERS ACCOUNT---------------------------------------------------- #
KarlU = secretManager.access_secret_version('kier-nonprod','KarlU','latest')
KarlP = secretManager.access_secret_version('kier-nonprod','KarlP','latest')

AimanU = secretManager.access_secret_version('kier-nonprod','AimanU','latest')
AimanP = secretManager.access_secret_version('kier-nonprod','AimanP','latest')

AndrewU = secretManager.access_secret_version('kier-nonprod','AndrewU','latest')
AndrewP = secretManager.access_secret_version('kier-nonprod','AndrewP','latest')

LuigiU = secretManager.access_secret_version('kier-nonprod','LuigiU','latest')
LuigiP = secretManager.access_secret_version('kier-nonprod','LuigiP','latest')

RebeccaU = secretManager.access_secret_version('kier-nonprod','RebeccaU','latest')
RebeccaP = secretManager.access_secret_version('kier-nonprod','RebeccaP','latest')

RobertU = secretManager.access_secret_version('kier-nonprod','RobertU','latest')
RobertP = secretManager.access_secret_version('kier-nonprod','RobertP','latest')

GTC_USER = secretManager.access_secret_version('kier-nonprod','GTC_USER','latest')
GTC_PASS = secretManager.access_secret_version('kier-nonprod','GTC_PASS','latest')

edit_u = secretManager.access_secret_version('kier-nonprod','edit_u','latest')
edit_p = secretManager.access_secret_version('kier-nonprod','edit_p','latest')

allan_email = secretManager.access_secret_version('kier-nonprod','allan_email','latest')
allan_password = secretManager.access_secret_version('kier-nonprod','allan_password','latest')

rich_u = secretManager.access_secret_version('kier-nonprod','rich_u','latest')
rich_p = secretManager.access_secret_version('kier-nonprod','rich_p','latest')

aiman_username = secretManager.access_secret_version('kier-nonprod','aiman_username','latest')
aiman_password = secretManager.access_secret_version('kier-nonprod','aiman_password','latest')

ellie_u = secretManager.access_secret_version('kier-nonprod','ellie_u','latest')
ellie_p = secretManager.access_secret_version('kier-nonprod','ellie_p','latest')

matt_u = secretManager.access_secret_version('kier-nonprod','matt_u','latest')
matt_p = secretManager.access_secret_version('kier-nonprod','matt_p','latest')

casey_u = secretManager.access_secret_version('kier-nonprod','casey_u','latest')
casey_p = secretManager.access_secret_version('kier-nonprod','casey_p','latest')

jose_u = secretManager.access_secret_version('kier-nonprod','jose_u','latest')
jose_p = secretManager.access_secret_version('kier-nonprod','jose_p','latest')

erin_u = secretManager.access_secret_version('kier-nonprod','erin_u','latest')
erin_p = secretManager.access_secret_version('kier-nonprod','erin_p','latest')

Tom_u = secretManager.access_secret_version('kier-nonprod','Tom_u','latest')
Tom_p = secretManager.access_secret_version('kier-nonprod','Tom_p','latest')

sergiu_u = secretManager.access_secret_version('kier-nonprod','sergiu_u','latest')
sergiu_p = secretManager.access_secret_version('kier-nonprod','sergiu_p','latest')

TomG_u = secretManager.access_secret_version('kier-nonprod','TomG_u','latest')
TomG_p = secretManager.access_secret_version('kier-nonprod','TomG_p','latest')

robertu = secretManager.access_secret_version('kier-nonprod','robertu','latest')
robertp = secretManager.access_secret_version('kier-nonprod','robertp','latest')

rebeccau = secretManager.access_secret_version('kier-nonprod','rebeccau','latest')
rebeccap = secretManager.access_secret_version('kier-nonprod','rebeccap','latest')

andrewu = secretManager.access_secret_version('kier-nonprod','andrewu','latest')
andrewp = secretManager.access_secret_version('kier-nonprod','andrewp','latest')

heliu = secretManager.access_secret_version('kier-nonprod','heliu','latest')
helip = secretManager.access_secret_version('kier-nonprod','helip','latest')
from facebook_business.adobjects.ad import Ad
from facebook_business.adobjects.lead import Lead
from facebook_business.api import FacebookAdsApi

access_token = 'EAAKXjRE07isBAMvf6PNYRuTJLK0JXAirAWKspexnyZAOl9hcNemKPC1hpiZBZCKELlczXV9t3XPTey4li704BL9O5vVJWvRnCO1zmA9Y1z80VQeATskCFRZAFcKH060sZAmlKmJdh60Q7f03bXfBbBws8kWZCiOjdjA2SgbSQZCc3NnmbSmjZAv4haX177b8DrYY2a2LYvtU5QZDZD'
app_secret = '53845d25235794979d44cfef77b5f02d'
app_id = '729582088285739'
id = '545564796967279'
FacebookAdsApi.init(access_token=access_token)

fields = [
]
params = {
  'filtering': [{'field':'time_created','operator':'LESS_THAN','value':1655653372}],
}
res = Ad(id).get_leads(
  fields=fields,
  params=params,
)

print(res)


import pandas as pd
from tabulate import tabulate
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.campaign import Campaign
from facebook_business.adobjects.adset import AdSet
from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.ad import Ad
import line_notify as ln

access_token = 'EAAfLtNSNQFcBAFE1HZA7p5s0vTZAkdKdlgCR2SbLprACDSbvdhydfOcc58d8sF816myRzQLAwFu0ZCieOWyT6xZAbWjZASGOSZB1Ww71zm9ygNKMu5azEWWhh5cvJBm0jQICcRZC9MdHP4Xn4FKZA7ASuZBs0mwOU5dEZD'
app_secret = '540e4c99f90cd8ec42466a8b46cf30a6'
app_id = '2194302357553239'
ad_account_id = 'act_490181464844435'
FacebookAdsApi.init(access_token=access_token)

translate_dic = {'ACTIVE' : '활성',
 'PAUSED' : '비활성',
 'DELETED' : '삭제됨',
 'PENDING_REVIEW' : '검토 중',
 'DISAPPROVED' : '승인되지 않음',
 'PREAPPROVED' : '예약됨',
 'PENDING_BILLING_INFO' : '결제문제로 대기',
 'CAMPAIGN_PAUSED' : '캠페인 중지',
 'ARCHIVED' : '삭제됨',
 'ADSET_PAUSED' : '광고세트 중지',
 'WITH_ISSUES' : '문제 있음'}

def fbdict_to_dict(fbdict):
    dic = {}
    for key in list(fbdict.keys()):
        if key in ['status', 'effective_status']:
            dic[key] = translate_dic[fbdict[key]]
        else:
            dic[key] = fbdict[key]
    return dic

def fbdict_list_to_dics_list(fbdict_list):
    dics_list = []
    for fbdict in fbdict_list:
        dic = fbdict_to_dict(fbdict)
        dics_list.append(dic)
    return dics_list

def getting_campaigns_all_status(ad_account_id, fields, params_ = {}):
    # Preset
    status = ['ACTIVE', 'PAUSED', 'DELETED', 'PENDING_REVIEW', 'DISAPPROVED', 'PREAPPROVED', 'PENDING_BILLING_INFO', 'CAMPAIGN_PAUSED', 'ARCHIVED', 'ADSET_PAUSED', 'WITH_ISSUES']
    params = {'effective_status': status}
    params.update(params_)
    # Main
    campaigns = AdAccount(ad_account_id).get_campaigns(fields=fields, params=params)
#     campaigns = fbdict_list_to_dics_list(campaigns)
    return fbdict_list_to_dics_list(campaigns)

def getting_adsets_by_campaign(campaign_id, fields):
    adsets = Campaign(campaign_id).get_ad_sets(fields = fields)
    return fbdict_list_to_dics_list(adsets)

def getting_adsets_and_an_ad_by_campaign(campaign_id, fields):
    adsets = Campaign(campaign_id).get_ad_sets(fields = fields)
    adsets = fbdict_list_to_dics_list(adsets)
    ad_fields = ['id', 'status', 'effective_status', 'issues_info']
    for adset in adsets:
        # Assuming there is just one ad
        ad = getting_ads_by_adset(adset['id'], ad_fields)[0]
        for field in ad_fields:
            try:
                adset['ad_' + field] = ad[field]
            except KeyError:
                pass
    return adsets

def getting_ads_by_adset(adset_id, fields):
    ads = AdSet(adset_id).get_ads(fields = fields)
    return fbdict_list_to_dics_list(ads)


campaign_id = '23843308835020636'
# campaign_id = '23843300409300636'
fields = ['id', 'name', 'status', 'effective_status', 'issues_info']
adsets = getting_adsets_and_an_ad_by_campaign(campaign_id, fields)

#보여주기
# pd.DataFrame(adsets, columns = fields)
# columns = ['name', 'status', 'effective_status', 'ad_status', 
#            'ad_effective_status', 'issues_info', 'ad_issues_info']
# print(pd.DataFrame(adsets, columns=columns))
# df = pd.DataFrame(adsets, columns=columns)
# print(tabulate(df, headers='keys', tablefmt='psql', floatfmt=",.0f"))

message = ''
for adset in adsets:
    if len(message) != 0:
        message += '\n'
    temp = '{} 광고는 현재 <{}> 상태입니다.'.format(adset['name'], adset['ad_effective_status'])
    message += temp

ln.send_line_msg(message)
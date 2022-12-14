import requests
import json
import random
from string import Template


tester_details=[]
insights=''  # To store the block_insights response
study_id='4def2733-f775-462b-a65f-2d20469064fe'
base_url='https://in.dev.apicx.getdecode.io/v1/'
login_url='https://app.dev.getdecode.io/authentication/login'
end_points1='tester'
end_points2=['test/blocks?study_id=$study_id&block_id=$block_id&tester_id=$tester','tester_response']
end_points_2=Template(end_points2[0])
end_points3=['studies/4def2733-f775-462b-a65f-2d20469064fe?is_insights=true','testers','testers',f'blocks?study_id={study_id}&block_id=99d22693-ed4f-4474-b42a-ffa89a519b49',f'blocks?study_id={study_id}&block_id=5a43eaba-8700-4524-9eb5-1fb09bba1e15','blocks_insights']

request_json={'username': "bantupalli.sriharsha@entropiktech.com", 'password': "Harsha@10150", 'workspace': "beintern"}
jsondata=json.dumps(request_json)
response=requests.post(login_url, data=jsondata)
assert response.status_code==200, 'Error'
c=response.content
c=json.loads(c.decode('utf-8'))
access_token=c['data']['access_token']
id_token=c['data']['id_token']
headers1= {'authorization': access_token, 'id_token': id_token, 'workspace_id': '01GG7AW75CHDNZ2BNYKZS9ZHMF'}



#To generate tester id using post method******************************************************************************************************
def call_tester_url(a):

    global tester_details
    global block_id
    global option_ids
    global tester
    
    url=a

    if(url==base_url+end_points1):
        request_json={"study_id":study_id,"workspace_id":headers1['workspace_id'],"preview":True,"variables":{}}
        jsondata=json.dumps(request_json)
        response=requests.post(url, headers=headers1, data=jsondata)
        assert response.status_code==200, 'Error'
        c=response.content
        c=json.loads(c.decode('utf-8'))
        tester=c['data']['tester']['tester_id']
        tester_details.append(tester)
        print()



#To generate block_id and option_id using get method**********************************************************************************************
def call_study_test_resp_url(a):

    global block_id
    global option_ids
    global tester

    url=a

    if(url==base_url+end_points2[0]):
        response=requests.get(url, headers=headers1)
        assert response.status_code==200, 'Error'
        c=response.content
        c=json.loads(c.decode('utf-8'))
        block_id=c['data']['block']['block_id']

        bt=c['data']['block']['block_type']
        if(bt =="SHORT_ANSWER" or bt=="PARAGRAPH"):
            option_ids=['Survey was good', 'product was good', 'survey was decent', 'product is not that good']
        
        elif(bt =="LIKE_DISLIKE" or bt=="LINEAR_SCALE" or bt=="SMILEY_RATING" or bt=="STAR_RATING" ):
            option_ids=c['data']['block']['block_properties']['scale']

        elif(bt=="CHECKBOX" or bt=="MCQ_BLOCK" or bt=="DROPDOWN"):
            l=len(c['data']['block']['block_properties']['options'])
            for i in range(l):
                option_ids.append(c['data']['block']['block_properties']['options'][i]['option_id'])

        else: #(For thankyou page)
            block_id="14d2b236-2727-46b6-b7d2-bfc5029109d2"
            option_ids=[]


##Calling tester_url by passing block_id and option_id as response using post method

    if(url==base_url+end_points2[1]):

        if(len(option_ids)>0):
            r=random.randint(0, len(option_ids)-1)
            request_json={"block_id":block_id,"study_id":study_id,"tester_id":tester,"response":[option_ids[r]]}
        else:
            request_json={"block_id":block_id,"study_id":study_id,"tester_id":tester,"response":option_ids}

        jsondata=json.dumps(request_json)

        response=requests.post(url, headers=headers1, data=jsondata)
        assert response.status_code==200, 'Error'


##calling block_insights urls************************************************************************************************************************
def call_insight_url(a):

    global block_id
    global insights

    url=a

    if(url==base_url+end_points3[0]):
        response=requests.get(url, headers=headers1)
        assert response.status_code==200, 'Error'
    if(url==base_url+end_points3[1]):
        request_json={"study_id":study_id,"get_all_testers":True,"integrate":True}
        jsondata=json.dumps(request_json)
        response=requests.post(url, headers=headers1, data=jsondata)
        assert response.status_code==200, 'Error'
    if(url==base_url+end_points3[2]):
        request_json={"study_id":study_id,"last_evaluated_key":None,"get_all_testers":True}
        jsondata=json.dumps(request_json)
        response=requests.post(url, headers=headers1, data=jsondata)
        assert response.status_code==200, 'Error'
    if(url==base_url+end_points3[3]):
        response=requests.get(url, headers=headers1)
    if(url==base_url+end_points3[4]):
        response=requests.get(url, headers=headers1)
        assert response.status_code==200, 'Error'
        c=response.content
        c=json.loads(c.decode('utf-8'))
        block_id=c['data']['block_id']
    if(url==base_url+end_points3[5]):
        request_json={"study_id":study_id,"block_id":block_id,"tester_ids":[]}
        jsondata=json.dumps(request_json)
        response=requests.post(url, headers=headers1, data=jsondata)
        assert response.status_code==200, 'Error'
        insights=response.content


#Function to call all the urls***********************************************************************************************************************
def calling_methods():

    global block_id
    global tester

    call_tester_url(base_url+end_points1)
    b=0


    for _ in range(18):
        end_points2[0]=end_points_2.substitute(study_id=study_id, block_id=block_id, tester=tester)
        call_study_test_resp_url(base_url+end_points2[b])
        b=b+1
        if(b>1):
            b=0   


    for i in range(6):
        call_insight_url(base_url+end_points3[i])


for  t in range(2):

    block_id='99d22693-ed4f-4474-b42a-ffa89a519b49'
    option_ids=[]
    tester=''

    print(f'Test no. {t+1} started.........')
    calling_methods()
    print(f'Test no. {t+1} done')
    print()


#Function to check if the total no. of responses are same as the no. of tester ids******************************************************************************
def comp_response():
    global insights
    global tester_details

    insights=json.loads(insights.decode('utf-8'))
    print('Insights: ',insights)
    print()
    print('Tester_details: ', tester_details)
    print()


    if(len(tester_details)==insights['data']['insights']['finished']['total']):
        print('Total no. of responses are same as the total no. of tester ids')

    else:
        print('Total no. of responses are not same as the total no. of tester ids')


comp_response()










    


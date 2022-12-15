import requests
import json
import random
from string import Template


tester_details=[]
insights=''  # To store the block_insights response
study_id='4def2733-f775-462b-a65f-2d20469064fe'
base_url='https://in.dev.apicx.getdecode.io/v1/'
login_url='https://app.dev.getdecode.io/authentication/login'
tester_url='tester'
study_url=['test/blocks?study_id=$study_id&block_id=$block_id&tester_id=$tester','tester_response']
study_url_2=Template(study_url[0])
insights_url='blocks_insights'

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

    if(url==base_url+tester_url):
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
    global blocker
    url=a

    if(url==base_url+study_url[0]):
        response=requests.get(url, headers=headers1)
        assert response.status_code==200, 'Error'
        c=response.content
        c=json.loads(c.decode('utf-8'))
        block_id=c['data']['block']['block_id']

        bt=c['data']['block']['block_type']
        if(bt =="SHORT_ANSWER" or bt=="PARAGRAPH"):
            option_ids=['Survey was good', 'product was good', 'survey was decent', 'product is not that good']
            blocker.append(block_id)

        elif(bt =="LIKE_DISLIKE" or bt=="LINEAR_SCALE" or bt=="SMILEY_RATING" or bt=="STAR_RATING" ):
            option_ids=c['data']['block']['block_properties']['scale']
            blocker.append(block_id)

        elif(bt=="CHECKBOX" or bt=="MCQ_BLOCK" or bt=="DROPDOWN"):
            l=len(c['data']['block']['block_properties']['options'])
            for i in range(l):
                option_ids.append(c['data']['block']['block_properties']['options'][i]['option_id'])
            
            blocker.append(block_id)

        else: #(For thankyou page)
            block_id="14d2b236-2727-46b6-b7d2-bfc5029109d2"
            option_ids=[]


##Calling tester_url by passing block_id and option_id as response using post method

    if(url==base_url+study_url[1]):

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
    global blocker
    global tester_details

    url=a

    for i in range(8):
        request_json={"study_id":study_id,"block_id":blocker[i],"tester_ids":[]}
        jsondata=json.dumps(request_json)
        response=requests.post(url, headers=headers1, data=jsondata)
        assert response.status_code==200, 'Error'
        insights=response.content
        insights=json.loads(insights.decode('utf-8'))
        print()
        if(i==0):
            print('Tester_details: ', tester_details)
            print("-------------------------------------------------------------------------------------------------------")
        print()
        if(len(tester_details)==insights['data']['insights']['finished']['total']):
            print(i+1,') Total no. of responses are same as the total no. of tester ids for', insights['data']['block_name'], 
            ',Total responses: ', insights['data']['insights']['finished']['total'])

        else:
            print(i+1,') Total no. of responses are not same as the total no. of tester ids for', insights['data']['block_name'], 
            ',Total responses: ', insights['data']['insights']['finished']['total'])

#Function to call all the methods***********************************************************************************************************************
def calling_methods():

    global block_id
    global tester

    call_tester_url(base_url+tester_url)
    b=0

    for _ in range(18):
        study_url[0]=study_url_2.substitute(study_id=study_id, block_id=block_id, tester=tester)
        call_study_test_resp_url(base_url+study_url[b])
        b=b+1
        if(b>1):
            b=0   


<<<<<<< HEAD
=======
    for i in range(6):
        call_insight_url(base_url+end_points3[i])

#Using the for loop to perform the test for n no. of testers
>>>>>>> 53e1a91ccb974336d3309bc05e1a79e338a3a760
for  t in range(2):

    block_id='99d22693-ed4f-4474-b42a-ffa89a519b49'
    blocker=[]
    option_ids=[]
    tester=''

    print(f'Test no. {t+1} started.........')
    calling_methods()
    print(f'Test no. {t+1} done')
    print()


call_insight_url(base_url+insights_url)

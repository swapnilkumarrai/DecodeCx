import requests
import json
import random
import sys
from string import Template


tester_details=[]
option_ids=[]
block_id_list=[]
number_of_blocks=9  # No. of blocks
number_of_testers=2  # No. of testers giving test
number_of_block_insights=8  # No. of block_insights
insights=''  # To store the block_insights response
study_id='4def2733-f775-462b-a65f-2d20469064fe'
base_url='https://in.dev.apicx.getdecode.io/v1/'
login_url='https://app.dev.getdecode.io/authentication/login'
tester_url='tester'
get_resp_url='test/blocks?study_id=$study_id&block_id=$block_id&tester_id=$tester'
get_resp_url_2=Template(get_resp_url)
post_resp_url='tester_response'
insights_url='blocks_insights'

def generate_headers():
    #To generater authorization id and id token

    if(len(sys.argv)==3):
        username=sys.argv[1]
        password=sys.argv[2]

    request_json={'username': username, 'password': password, 'workspace': "beintern"}
    jsondata=json.dumps(request_json)
    response=requests.post(login_url, data=jsondata)
    assert response.status_code==200, 'Error'
    c=response.content
    c=json.loads(c.decode('utf-8'))
    access_token=c['data']['access_token']
    id_token=c['data']['id_token']

    return {'authorization': access_token, 'id_token': id_token, 'workspace_id': '01GG7AW75CHDNZ2BNYKZS9ZHMF'}


def generate_testers(url):
    #To generate tester id using post method
    global tester_details
    global tester

    request_json={"study_id":study_id,"workspace_id":headers1['workspace_id'],"preview":True,"variables":{}}
    jsondata=json.dumps(request_json)
    response=requests.post(url, headers=headers1, data=jsondata)
    assert response.status_code==200, 'Error'
    c=response.content
    c=json.loads(c.decode('utf-8'))
    tester=c['data']['tester']['tester_id']
    tester_details.append(tester)
    print()

    
def generate_block_options(url):
    #To generate block_id and option_id using get method
    global block_id
    global option_ids
    global block_id_list
    option=[]

    response=requests.get(url, headers=headers1)
    assert response.status_code==200, 'Error'
    c=response.content
    c=json.loads(c.decode('utf-8'))
    block_id=c['data']['block']['block_id']
    bt=c['data']['block']['block_type']

    if(bt =="SHORT_ANSWER" or bt=="PARAGRAPH"):
        option_ids.append(['Survey was good', 'product was good', 'survey was decent', 'product is not that good'])
        block_id_list.append(block_id)
    elif(bt =="LIKE_DISLIKE" or bt=="LINEAR_SCALE" or bt=="SMILEY_RATING" or bt=="STAR_RATING" ):
        option_ids.append(c['data']['block']['block_properties']['scale'])
        block_id_list.append(block_id)
    elif(bt=="CHECKBOX" or bt=="MCQ_BLOCK" or bt=="DROPDOWN"):
        l=len(c['data']['block']['block_properties']['options'])
        for i in range(l):
            option.append(c['data']['block']['block_properties']['options'][i]['option_id'])
        
        option_ids.append(option)
        block_id_list.append(block_id)
    else: #(For thankyou page)
        block_id="14d2b236-2727-46b6-b7d2-bfc5029109d2"
        block_id_list.append(block_id)


def pass_response(url):
    #Calling tester_url by passing block_id and option_id as response using post method
    global block_index
    global option_index
    block_index=block_index+1

    if(option_index<8):
        r=random.randint(0, len(option_ids[option_index])-1)
        request_json={"block_id":block_id_list[block_index],"study_id":study_id,"tester_id":tester,"response":[option_ids[option_index][r]]}
    else:
        request_json={"block_id":block_id_list[block_index],"study_id":study_id,"tester_id":tester,"response":[]}

    jsondata=json.dumps(request_json)
    response=requests.post(url, headers=headers1, data=jsondata)
    assert response.status_code==200, 'Error'
    option_index=option_index+1



def call_insight_url(url):
    #calling block_insights urls
    global insights
    
    for i in range(number_of_block_insights):
        request_json={"study_id":study_id,"block_id":block_id_list[i+1],"tester_ids":[]}
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


def calling_methods():
    #Function to call all the methods
    generate_testers(base_url+tester_url)

    for _ in range(number_of_blocks):
        if(t==0):
            get_resp_url=get_resp_url_2.substitute(study_id=study_id, block_id=block_id_list[block_index], tester=tester)
            generate_block_options(base_url+get_resp_url)

        pass_response(base_url+post_resp_url) 


if __name__=='__main__':

    headers1=generate_headers()

    for  t in range(number_of_testers):
        option_index=0
        block_index=0
        if(t==0):
            block_id_list.append('99d22693-ed4f-4474-b42a-ffa89a519b49')

        tester=''
        print(f'Test no. {t+1} started.........')
        calling_methods()
        print(f'Test no. {t+1} done')
        print()

    call_insight_url(base_url+insights_url)

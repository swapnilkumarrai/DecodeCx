import requests
import json
import random
from string import Template


tester_details=[]
r=''  # To save the value of block_insights response
study_id='4def2733-f775-462b-a65f-2d20469064fe'
base_url='https://in.dev.apicx.getdecode.io/v1/'
headers1= {'authorization': 'eyJraWQiOiJLOWlYZDlPMWJFcituUnBiWTR1U3JhM0I0SlFMd01lR1l2RUhlMjA1OWtFPSIsImFsZyI6IlJTMjU2In0.eyJzdWIiOiIzYWUwNWU5Mi0wZTNmLTRiZjQtODk2Yy0wNDYyNTA0YmEwNmEiLCJpc3MiOiJodHRwczpcL1wvY29nbml0by1pZHAuYXAtc291dGhlYXN0LTEuYW1hem9uYXdzLmNvbVwvYXAtc291dGhlYXN0LTFfRHBGT0xDVWhNIiwiY2xpZW50X2lkIjoiMnRoODU2aWFmaG5sZThndGZjbzFuZjdtMSIsIm9yaWdpbl9qdGkiOiIwZTVhYzFhYi00NWNmLTQwNjctOGQ1MC1kOTRmMzIyMzMzODgiLCJldmVudF9pZCI6Ijk5MWFkNGFmLTEwZjMtNGM4Zi1hOWNkLTM3ZWM2M2I5ZmEzOSIsInRva2VuX3VzZSI6ImFjY2VzcyIsInNjb3BlIjoiYXdzLmNvZ25pdG8uc2lnbmluLnVzZXIuYWRtaW4iLCJhdXRoX3RpbWUiOjE2Njk4NzE0MDcsImV4cCI6MTY2OTg3NTAwNiwiaWF0IjoxNjY5ODcxNDA3LCJqdGkiOiI4NjQzMmNkZS00MGY5LTQ4MzUtYjgzOS0xYTM0MGQwNDllY2UiLCJ1c2VybmFtZSI6IjNhZTA1ZTkyLTBlM2YtNGJmNC04OTZjLTA0NjI1MDRiYTA2YSJ9.XqGlxvvRfOf6LWJnPXODKKxw7FzALB247ZcxcK7rA-oTsbeArZmGS1eH7Dox8IjJMmjfDhlMQRZreS9uEV_u8NkN4zF1gTYFqav5w-ZIi4Tp04Svd2kYtK2XVOrme_PBMTi6Y7pSqRBILyDOl1DsyUQyekqlNwHf-kEIssujU5cV3iHTfAKoXiv006jApg5sq62hPnXCcXURy30MYNsKqEQ3FvEq26-jkGpAON6akU1LmmsYyD2qdsvUYLTEoHy6cfzI1gwJHKglrmKEs6ESkpJtrnPxXMuELOK-lgUZnHrv3-cPeECGziQn2Ps7VlfY2cqCwdGzIukEqLhi3VsJiQ',
    'id_token': 'eyJraWQiOiJha1BwMHpKbFJqXC9ZYWpac1dTbGhmRFwvclVSRHdJT2lEMUYrRGxtOWFKQXM9IiwiYWxnIjoiUlMyNTYifQ.eyJzdWIiOiIzYWUwNWU5Mi0wZTNmLTRiZjQtODk2Yy0wNDYyNTA0YmEwNmEiLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwiaXNzIjoiaHR0cHM6XC9cL2NvZ25pdG8taWRwLmFwLXNvdXRoZWFzdC0xLmFtYXpvbmF3cy5jb21cL2FwLXNvdXRoZWFzdC0xX0RwRk9MQ1VoTSIsImNvZ25pdG86dXNlcm5hbWUiOiIzYWUwNWU5Mi0wZTNmLTRiZjQtODk2Yy0wNDYyNTA0YmEwNmEiLCJvcmlnaW5fanRpIjoiMGU1YWMxYWItNDVjZi00MDY3LThkNTAtZDk0ZjMyMjMzMzg4IiwiYXVkIjoiMnRoODU2aWFmaG5sZThndGZjbzFuZjdtMSIsImV2ZW50X2lkIjoiOTkxYWQ0YWYtMTBmMy00YzhmLWE5Y2QtMzdlYzYzYjlmYTM5IiwidXNlcl9pZCI6IjAxR0c3QVZBUFkwQjlGWVRLTUYzUkpEM1pHIiwidG9rZW5fdXNlIjoiaWQiLCJhdXRoX3RpbWUiOjE2Njk4NzE0MDcsImV4cCI6MTY2OTg3NTAwNiwiaWF0IjoxNjY5ODcxNDA3LCJqdGkiOiJiZTNiNDU5Ny04NDk2LTQ1ZTMtYTQ0MS1hY2I1MjViYjkyZjAiLCJlbWFpbCI6ImJhbnR1cGFsbGkuc3JpaGFyc2hhQGVudHJvcGlrdGVjaC5jb20ifQ.AFqzaqzidFOvsrELzj2ZdCY7T8PKSmsPxbpiE6AnT18N4PQafucVIh0_3U7eyRryswnazLCKcrsn8NtoFf_FWKE0vd00HhfeOnkpT7EIYzo0EsbybJatwh1sssDOWwiBlqIc_qPoDYGCmUL-SxnEpKlNQsDzQwtDecL7sEnXKGmI-NxNkJjkPwQF6jy7rQ4vwmR97gPa09r5IlkFJWnoRo9FpTdyj6fw_tQdAJCCBEEMlO6_xeuPyyEtCNgoWl3v3E8jjfupGITBdhKhci1MpYeyLSYWFvcKvRN2WNMIw9tE8kSch3tHSWXb1fwHcYuqz1AAA3qcWfyWyUV8GA_2Pg',
    'workspace_id': '01GG7AW75CHDNZ2BNYKZS9ZHMF'}

end_points1='tester'
end_points2=['test/blocks?study_id=$study_id&block_id=$block_id&tester_id=$tester','tester_response']
end_points_2=Template(end_points2[0])
end_points3=['studies/4def2733-f775-462b-a65f-2d20469064fe?is_insights=true','testers','testers',f'blocks?study_id={study_id}&block_id=99d22693-ed4f-4474-b42a-ffa89a519b49',f'blocks?study_id={study_id}&block_id=5a43eaba-8700-4524-9eb5-1fb09bba1e15','blocks_insights']

for  t in range(2):

    block_id='99d22693-ed4f-4474-b42a-ffa89a519b49'
    option_ids=[]
    tester=''


#To generate tester id using post method******************************************************************************************************
    def call_tester_url(a):

        global tester_details
        global block_id
        global option_ids
        global tester
        global r
        
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
    def call_study_tester_url(a):

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
        global r

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
            r=response.content


    #Function to call all the urls***********************************************************************************************************************
    def calling_urls():

        global block_id
        global tester

        call_tester_url(base_url+end_points1)
        b=0


        for _ in range(18):
            end_points2[0]=end_points_2.substitute(study_id=study_id, block_id=block_id, tester=tester)
            call_study_tester_url(base_url+end_points2[b])
            b=b+1
            if(b>1):
                b=0   


        for i in range(6):
            call_insight_url(base_url+end_points3[i])


    print(f'Test no. {t+1} started.........')
    calling_urls()
    print(f'Test no. {t+1} done')
    print()


#Function to check if the total no. of responses are same as the no. of tester ids******************************************************************************
def comp_response():
    global r
    global tester_details

    r=json.loads(r.decode('utf-8'))
    print('Insights: ',r)
    print()
    print('Tester_details: ', tester_details)
    print()


    if(len(tester_details)==r['data']['insights']['finished']['total']):
        print('Total no. of responses are same as the total no. of tester ids')

    else:
        print('Total no. of responses are not same as the total no. of tester ids')



    

comp_response()










    


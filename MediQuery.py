# First
import openai 
import streamlit as st
from dotenv import load_dotenv
import os
import re
from bs4 import BeautifulSoup
import html2text
import requests
from serpapi import GoogleSearch
from openai import OpenAI
# client = OpenAI()
import streamlit as st
from streamlit.logger import get_logger

# LOGGER = get_logger(__name__)

# streamlit config show
def run():
    st.set_page_config(
        page_title="MediQuery",
        page_icon="🧑‍🎓",
    )
    with st.sidebar:
        openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
        client = OpenAI(api_key = openai_api_key)
        "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"
    st.title("💬 Health Helper") 
    if "messages" not in st.session_state:
        st.session_state["messages"] = [{"role": "assistant", "content": "What would you like to ask?"}]

    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    if prompt := st.chat_input():
        if not openai_api_key:
            st.info("Please add your OpenAI API key to continue.")
            st.stop()
        client = OpenAI(api_key = openai_api_key)
        openai.api_key = openai_api_key
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)
    # main.py \/\/\/

        load_dotenv()
        # openai.api_key = "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"

        searchQuery = prompt
        questionExample2 = prompt
        searchQuery += " National Institutes of Health (.gov)"

        params = {
        "engine": "google",
        "q": searchQuery,
        "hl": "en",
        "gl": "us",
        "google_domain": "google.com",
        "num": "10",
        "start": "0",
        "safe": "active",
        "api_key": "7bf0360cf2e3f0c4258016f7f41dd9dba39c3752234c78e7e87f2f5ebe9de759"
        }

        search = GoogleSearch(params)

        results = search.get_dict()
        organic_results = results["organic_results"]

        def reorganize_json_for_gov_sources(json_data):
            # """
            # Reorganizes JSON data to include only entries from .gov websites.
            # The position of the entry is used as the key, and the link as the value.

            # Parameters:
            # json_data (list): A list of dictionaries representing the JSON data.

            # Returns:
            # dict: A dictionary with positions as keys and links as values for .gov sources.
            # """
            gov_sources = {}
            for item in json_data:
                if '.gov' in item['source']:
                    gov_sources[item['position']] = item['link']
            return gov_sources

        reorganized_data = reorganize_json_for_gov_sources(organic_results)
    
        def scraper123(reorganized_datas, number):
            payload = {'api_key': 'ae89d50aea92ebfd2bb9cbfd6bc53524', 'url': reorganized_datas.get(number)}
            r = requests.get('http://api.scraperapi.com', params=payload)
            html_code = r.text
            text = html2text.html2text(html_code)
            site = reorganized_datas.get(number)
            return r, html_code, text, site
        def nsdUpdater(nsd2):
            nsd2.update({"abstract": " "})
            nsd2.update({"introduction": " "})
            nsd2.update({"study results": " "})
            nsd2.update({"discussion": " "})
            nsd2.update({"conclusion": " "})
            nsd2.update({"methods": " "})
            nsd2.update({"references": " "})
            nsd2.update({"funding statement": " "})
            nsd2.update({"author contribution": " "})
            nsd2.update({"potential conflicts of interest": " "})    
        # def dataOrganizer(dataList, partData, nsd2):
        #     for part in dataList:
        #         if  nsd2[part] != None:
        #             partData[part] = nsd2[part]    
        def dataOrganizer(dataList, partData, nsd2):
            for part in dataList:
                try:
                    nsd2[part]
                except:
                    # Code to execute if the variable does not exist
                    partData[part] = " "
                    # Add your action here
                else:
                    partData[part] = nsd2[part]
        def textSplitAndReorganizer(r, text):
            html_code = r.text

            text = html2text.html2text(html_code)

            section_re = r"(## .+?\n)(.+?)(?=\n## |$)"

            # Extracting all sections
            sections = re.findall(section_re, text, re.DOTALL)

            # Storing the sections in a dictionary where the key is the section title and the value is the section content
            section_dict = {title.strip(): content.strip() for title, content in sections}

            nsd = {}
            nsd_l = []

            for key in section_dict:
                nsd[key.lower()]=section_dict[key]
        
            for key in nsd:
                nsd_l.append(key)

            x = str(nsd_l)

            # st.write(x)
            nsdhelper1 = client.chat.completions.create(
                    model="gpt-4-1106-preview",
                    messages=[{"role":"system", "content": "given a python list containing keys to the python dictionary nsd, match the keys EXACTLY into any of the following standardized names, remove any other characters: abstract, introduction, study results, discussion, conclusion, methods, references, funding statement, author contribution, potential conflicts of interest. Make sure to accurately assign from the keys of nsd, misspellings can be harmful. Note that not all names must be used NOT ALL MUST BE MAPPED, and it may not always be obvious which key should be assigned which name. If there is no valid mapping found for the given key, do not include it. DO NOT DUPLICATE ANYTHING. NO OTHER TEXT WHATSOEVER."},
                            {"role":"user", "content": "['## account', '## abstract', '## 1\\. introduction', '## methods', '## study results', '## discussion', '## conclusion', '## appendix 1.', '## funding statement', '## author contribution', '## disclosure of potential conflicts of interest', '## references']"},
                            {"role":"assistant", "content": """
                "abstract"<-'## abstract',
                "introduction"<-'## 1\\. introduction',
                "study results"<-'## study results',
                "discussion"<-'## discussion',
                "conclusion"<-'## conclusion',
                "methods"<-'## methods',
                "refrences"<-'## references',
                "funding statement"<-'## funding statement',
                "author contributions"<-'## author contribution',
                "potential conflicts of interest"<-'## disclosure of potential conflicts of interest',
                """
                            },
                            {"role":"user", "content": "['## account', '## overview', '## opening', '## techniques', '## research findings', '## interpretations', '## final thoughts', '## supplementary 1.', '## funding acknowledgment', '## author involvement', '## declaration of potential conflicts of interest', '## literature']" },
                            {"role":"assistant", "content": """
                "abstract" <- '## overview',
                "introduction" <- '## opening',
                "study results" <- '## research findings',
                "discussion" <- '## discussion',
                "conclusion" <- '## final thoughts',
                "methods" <- '## techniques',
                "refrences" <- '## references',
                "funding statement" <- '## funding acknowledgment',
                "author contributions" <- '## author involvement',
                "potential conflicts of interest" <- '## declaration of potential conflicts of interest'
                """
                            },
                            {"role":"user", "content": x }           
                            ]
                )
            y = nsdhelper1.choices[0].message.content
            # st.write(y)
            nsdhelper = client.chat.completions.create(
                    model="gpt-4-1106-preview",
                    messages=[{"role":"system", "content": "given a list of matched python keys to the python dictionary nsd2, recreate nsd2 with the keys all renamed EXACTLY as they are mapped. Make sure to accurately assign the keys of nsd2, misspellings can be harmful. DO NOT DUPLICATE ANYTHING. OUTPUT MUST ONLY BE THE PYTHON CODE, NO OTHER TEXT WHATSOEVER. NO INDENTS. RESPONSE MUST BE EXECUTABLE. DO NOT APOLOGIZE, SAY HERE IS THE..., OR ADD ANY OTHER TEXT OTHER THAN THE PYTHON CODE. MUST EXCLUSIVELY OUTPUT EXECUTABLE PYTHON CODE. "},
                            # Given a dictionary 'nsd' and a list of key mappings, create a new dictionary 'nsd2' where each key in 'nsd' is renamed according to the mapping. Ensure the keys in 'nsd2' match the mappings exactly. The output should be clean, executable Python code that recreates 'nsd2' with the new key names, without any additional text, comments, or unnecessary indentations."
                            {"role":"user", "content": """
                "abstract"<-'## abstract',
                "introduction"<-'## introduction',
                "study results"<-'## study results',
                "discussion"<-'## discussion',
                "conclusion"<-'## conclusion',
                "methods"<-'## methods',
                "refrences"<-'## references',
                "funding statement"<-'## funding statement',
                "author contributions"<-'## author contribution',
                "potential conflicts of interest"<-'## disclosure of potential conflicts of interest',
                """
                            },
                            {"role":"assistant", "content": """
    nsd2 = {
        "abstract": nsd['## abstract'],
        "introduction": nsd['## introduction'],
        "study results": nsd['## study results'],
        "discussion": nsd['## discussion'],
        "conclusion": nsd['## conclusion'],
        "methods": nsd['## methods'],
        "refrences": nsd['## references'],
        "funding statement": nsd['## funding statement'],
        "author contributions": nsd['## author contribution'],
        "potential conflicts of interest": nsd['## disclosure of potential conflicts of interest'],
        }
            """
                            },
                            {"role":"user", "content": """
                "abstract" <- '## overview',
                "introduction" <- '## opening',
                "study results" <- '## research findings',
                "discussion" <- '## discussion',
                "conclusion" <- '## final thoughts',
                "methods" <- '## techniques',
                "refrences" <- '## references',
                "funding statement" <- '## funding acknowledgment',
                "author contributions" <- '## author involvement',
                "potential conflicts of interest" <- '## declaration of potential conflicts of interest'
                """
                            },
                            {"role":"assistant", "content": """
    nsd2 = {
        "abstract": nsd['## overview'],
        "introduction": nsd['## opening'],
        "study results": nsd['## research findings'],
        "discussion": nsd['## discussion'],
        "conclusion": nsd['## final thoughts'],
        "methods": nsd['## techniques'],
        "refrences": nsd['## references'],
        "funding statement": nsd['## funding acknowledgment'],
        "author contributions": nsd['## author involvement'],
        "potential conflicts of interest": nsd['## declaration of potential conflicts of interest']
        }"""
                            },
                            {"role":"user", "content": y }           
                            ]
                )

            xy = str(nsdhelper.choices[0].message.content)
            return xy, nsd
        # cIterator = 1
        # while cIterator <= len(reorganized_data):
        #     fgh, ghf, trt = scraper123(reorganized_data, cIterator)
        #     # print(trt)
        #     cIterator += 1

        checkerNum = 0
        checkerIterator = 1

        while int(checkerNum) < 1:
            if checkerIterator > len(reorganized_data):
                "code Failed"
                break
            r, html_code, text, site = scraper123(reorganized_data, checkerIterator)
            checkerIterator += 1
            checkerInput = "Can You Answer the question, " + questionExample2 + ", exclusively interpreting the following abstract, introduction, study results, discussion, and conclusion of the provided research paper. output 0 for no or 1 for yes. DO NOT OUTPUT ANYTHING ELSE."
            xy1, nsd = textSplitAndReorganizer(r, text)
            # st.write(xy1)
            # keep while try except the name error
            execChecker = False
            for i in range(10):
                try:
                    xy1, nsd = textSplitAndReorganizer(r, text)
                    # st.write(xy1)
                    exec(xy1)
                except:
                    # Code to execute if the variable does not exist
                    # st.write(f"KeyError encountered at attempt {i+1}")
                    # print(f"KeyError encountered at attempt {i+1}")
                    continue
                else:
                    execChecker = True
                    break

            # if not execChecker:
            #     st.write("execChecker failed")
            #     print("execChecker failed")
                

            
            # nsdUpdater(nsd2)
            cD1 = {}
            cDL1 = ["abstract", "introduction", "study results", "discussion", "conclusion"]
            dataOrganizer(cDL1, cD1, nsd2)
            # print("break1")  
            # st.write(checkerInput)      
            # print(cD1)
            # openai.api_key = "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"
            # client.chat.completions.create(
            #     model="gpt-3.5-turbo-1106",
            #     messages=[
            #         {
            #         "role": "system",
            #         "content":                },
            #         {
            #         "role": "user",
            #         "content":                 
            #         },
            #         {
            #         "role": "assistant",
            #         "content": "1"
            #         }
            #     ],
            #     temperature=1,
            #     max_tokens=4095,
            #     top_p=1,
            #     frequency_penalty=0,
            #     presence_penalty=0
            #     )
            
            checker = client.chat.completions.create(
                model="gpt-4-1106-preview",
                messages=[
                        {"role":"system", "content": str(checkerInput)},
                        {"role":"user", "content": str(cD1) },
                        ],
                temperature=1,
                max_tokens=4095,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0
            )
            
            # print("break2")    



                
            checkerNum = int(checker.choices[0].message.content)
            # st.write(checkerNum)
        # html_code = r.text

        # text = html2text.html2text(html_code)

        # section_re = r"(## .+?\n)(.+?)(?=\n## |$)"

        # # Extracting all sections
        # sections = re.findall(section_re, text, re.DOTALL)

        # # Storing the sections in a dictionary where the key is the section title and the value is the section content
        # section_dict = {title.strip(): content.strip() for title, content in sections}

        # nsd = {}
        # nsd_l = []

        # for key in section_dict:
        #     nsd[key.lower()]=section_dict[key]
    
        # for key in nsd:
        #     nsd_l.append(key)

        # x = str(nsd_l)

        # st.write(x)
        # nsdhelper1 = openai.ChatCompletion.create(
        #         model="gpt-3.5-turbo",
        #         messages=[{"role":"system", "content": "given a python list containing keys to the python dictionary nsd, match the keys EXACTLY into any of the following standardized names, remove any other characters: abstract, introduction, study results, discussion, conclusion, methods, references, funding statement, author contribution, potential conflicts of interest. Make sure to accurately assign from the keys of nsd, misspellings can be harmful. Note that not all names must be used, and it may not always be obvious which key should be assigned which name. DO NOT DUPLICATE ANYTHING. NO OTHER TEXT WHATSOEVER."},
        #                 {"role":"user", "content": "['## account', '## abstract', '## 1\\. introduction', '## methods', '## study results', '## discussion', '## conclusion', '## appendix 1.', '## funding statement', '## author contribution', '## disclosure of potential conflicts of interest', '## references']"},
        #                 {"role":"assistant", "content": """
        #     "abstract"<-'## abstract',
        #     "introduction"<-'## introduction',
        #     "study results"<-'## study results',
        #     "discussion"<-'## discussion',
        #     "conclusion"<-'## conclusion',
        #     "methods"<-'## methods',
        #     "refrences"<-'## references',
        #     "funding statement"<-'## funding statement',
        #     "author contributions"<-'## author contribution',
        #     "potential conflicts of interest"<-'## disclosure of potential conflicts of interest',
        #     """
        #                 },
        #                 {"role":"user", "content": "['## account', '## overview', '## opening', '## techniques', '## research findings', '## interpretations', '## final thoughts', '## supplementary 1.', '## funding acknowledgment', '## author involvement', '## declaration of potential conflicts of interest', '## literature']" },
        #                 {"role":"assistant", "content": """
        #     "abstract" <- '## overview',
        #     "introduction" <- '## opening',
        #     "study results" <- '## research findings',
        #     "discussion" <- '## discussion',
        #     "conclusion" <- '## final thoughts',
        #     "methods" <- '## techniques',
        #     "refrences" <- '## references',
        #     "funding statement" <- '## funding acknowledgment',
        #     "author contributions" <- '## author involvement',
        #     "potential conflicts of interest" <- '## declaration of potential conflicts of interest'
        #     """
        #                 },
        #                 {"role":"user", "content": x }           
        #                 ]
        #     )
        # y = nsdhelper1.choices[0].message.content
        # st.write(y)
        # nsdhelper = openai.ChatCompletion.create(
        #         model="gpt-3.5-turbo",
        #         messages=[{"role":"system", "content": "given a list of matched python keys to the python dictionary nsd2, recreate nsd2 with the keys all renamed EXACTLY as they are mapped. Make sure to accurately assign the keys of nsd2, misspellings can be harmful. DO NOT DUPLICATE ANYTHING. OUTPUT MUST ONLY BE THE PYTHON CODE, NO OTHER TEXT WHATSOEVER. NO INDENTS. RESPONSE MUST BE EXECUTABLE."},
        #                 {"role":"user", "content": """
        #     "abstract"<-'## abstract',
        #     "introduction"<-'## introduction',
        #     "study results"<-'## study results',
        #     "discussion"<-'## discussion',
        #     "conclusion"<-'## conclusion',
        #     "methods"<-'## methods',
        #     "refrences"<-'## references',
        #     "funding statement"<-'## funding statement',
        #     "author contributions"<-'## author contribution',
        #     "potential conflicts of interest"<-'## disclosure of potential conflicts of interest',
        #     """
        #                 },
        #                 {"role":"assistant", "content": """
        # nsd2 = {
        #     "abstract": nsd['## abstract'],
        #     "introduction": nsd['## introduction'],
        #     "study results": nsd['## study results'],
        #     "discussion": nsd['## discussion'],
        #     "conclusion": nsd['## conclusion'],
        #     "methods": nsd['## methods'],
        #     "refrences": nsd['## references'],
        #     "funding statement": nsd['## funding statement'],
        #     "author contributions": nsd['## author contribution'],
        #     "potential conflicts of interest": nsd['## disclosure of potential conflicts of interest'],
        #     }
        #     """
        #                 },
        #                 {"role":"user", "content": """
        #     "abstract" <- '## overview',
        #     "introduction" <- '## opening',
        #     "study results" <- '## research findings',
        #     "discussion" <- '## discussion',
        #     "conclusion" <- '## final thoughts',
        #     "methods" <- '## techniques',
        #     "refrences" <- '## references',
        #     "funding statement" <- '## funding acknowledgment',
        #     "author contributions" <- '## author involvement',
        #     "potential conflicts of interest" <- '## declaration of potential conflicts of interest'
        #     """
        #                 },
        #                 {"role":"assistant", "content": """
        # nsd2 = {
        #     "abstract": nsd['## overview'],
        #     "introduction": nsd['## opening'],
        #     "study results": nsd['## research findings'],
        #     "discussion": nsd['## discussion'],
        #     "conclusion": nsd['## final thoughts'],
        #     "methods": nsd['## techniques'],
        #     "refrences": nsd['## references'],
        #     "funding statement": nsd['## funding acknowledgment'],
        #     "author contributions": nsd['## author involvement'],
        #     "potential conflicts of interest": nsd['## declaration of potential conflicts of interest']
        #     }"""
        #                 },
        #                 {"role":"user", "content": y }           
        #                 ]
        #     )

        # xy = str(nsdhelper.choices[0].message.content)
        xy, nsd = textSplitAndReorganizer(r, text)
        # st.write(xy)
        exec(xy)
        nsdUpdater(nsd2)
        # nsd2.update({"abstract": " "})
        # nsd2.update({"introduction": " "})
        # nsd2.update({"study results": " "})
        # nsd2.update({"discussion": " "})
        # nsd2.update({"conclusion": " "})
        # nsd2.update({"methods": " "})
        # nsd2.update({"references": " "})
        # nsd2.update({"funding statement": " "})
        # nsd2.update({"author contribution": " "})
        # nsd2.update({"potential conflicts of interest": " "})

        
                    
        claimData = {}
        claimDataList = ["abstract", "introduction", "study results", "discussion", "conclusion"]
        dataOrganizer(claimDataList, claimData, nsd2)

        evidenceData = {}
        evidenceDataList = ["methods", "discussion", "study results"]
        dataOrganizer(evidenceDataList, evidenceData, nsd2)

        reasoningData = {}
        reasoningDataList = ["methods", "discussion", "study results", "conclusion"]
        dataOrganizer(reasoningDataList, reasoningData, nsd2)

        biasData = {}
        biasDataList = ["funding statement", "author contribution", "potential conflicts of interest", "references"]
        dataOrganizer(biasDataList, biasData, nsd2)

        biasDataString = str(biasData)

        def claimQuestionFormatter(questionExample, claimData):
            if questionExample[0] != "\"":
                questionExample = "\"" + questionExample + "\""
            if questionExample[0] != "Q":
                questionExample = "Question: " + questionExample
            pQE= questionExample + "\n" + "\n" + str(claimData)
            return pQE

        pQE2 = claimQuestionFormatter(questionExample2, claimData)

        claim = client.chat.completions.create(
            model="gpt-3.5-turbo-16k",
            messages=[
                    {"role":"system", "content": "In a 2 sentence response: Answer the question exclusively using the following abstract, introduction, study results, discussion, and conclusion of a research paper. Start your response with a direct answer to the question (ex. No, the research paper reviewed in this response suggests that consuming certain types of dairy, including milk, yogurt, and kefir, may actually have a positive effect on the gut microbiota by promoting the growth of beneficial bacteria. However, the impact of dairy consumption on the gut microbiota is still not fully understood and further studies are needed to determine the optimal quantity and long-term effects of dairy consumption on gut bacteria.)"},
                    {"role":"user", "content": pQE2 }
                    ]
        )

        claimResponse = str(claim.choices[0].message.content)
        pqeReset=pQE2

        def evidenceQuestionFormatter(questionExample):
            if questionExample[0] != "\"":
                questionExample = "\"" + questionExample + "\""
            if questionExample[0] != "Q":
                questionExample = "Question: " + questionExample
            pQE= questionExample + "\n" + "\n" + str(evidenceData)
            return pQE

        eqe = evidenceQuestionFormatter(questionExample2)

        evidenceInput = eqe + "\n" + "\n" + "Claim: "+str(claimResponse)

        evidence = client.chat.completions.create(
            model="gpt-3.5-turbo-16k",
            messages=[
                    {"role":"system", "content": "In a 3 sentence response: Provide evidence to the claim part of the response (provided below the paper)  to the question (at the top) exclusively using the provided methods, study results, discussion, and references of a research paper. "},
                    {"role":"user", "content": evidenceInput }
                    ]
        )

        evidenceResponse = str(evidence.choices[0].message.content)
        # answerPart1 = str("\n" + claimResponse)
        answer = "  \n" + claimResponse + "  \n",evidenceResponse + "  \nThis Result was supplied with information obtained from the following research Paper:\n" + str(site) #potential break
        answer = str(answer) # test
        msg = {
            "role": "assistant",
            "content": answer
            }
        st.session_state.messages.append(msg)
        st.chat_message("assistant").write(msg["content"])
if __name__ == "__main__":
    run()
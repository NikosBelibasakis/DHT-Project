import aiohttp
import asyncio
import json
from bs4 import BeautifulSoup

# Function which returns last word
def lastWord(string):
    # split by space and converting
    # string to list and
    lis = list(string.split(" "))

    # length of list
    length = len(lis)

    # returning last element in list
    return lis[length - 1]

def table_award_search(soup):
    awards_found = 0
    awards_number = 0
    # find the computer scientist's wikipedia table
    table = soup.find('table', class_='infobox biography vcard')

    # check if there is no scientist's wikipedia table

    if (table is None):
        return 0;

    # if there is a scientist's wikipedia table
    else:

        # find all the <th> tags in the table
        th_temp = table.find_all('th')
        for t in th_temp:
            # check if any of these <th> tags contains the 'Awards' word
            if 'Awards' in t.text:
                awards_found = 1   #there is a table header that contains the 'Awards' word
                tr_temp = t.find_previous('tr')


        if(awards_found == 1):
              ul_temp = tr_temp.find_all('ul')  #check if there is at least one list (<ul> tag) in the 'Awards' table row

              if (ul_temp):  # if there is at least one list in the 'Awards' row
                   for u in ul_temp:
                     li_temp = u.find_all('li')  #find all the <li> tags in each <ul> tag
                     awards_number = awards_number + len(li_temp) #each <li> tag found is an award




              else:           #no list found (<ul> tag), we will search for the number of <br> tags in the table row data (<td> tag)
                    br_temp = tr_temp.find_all('br')
                    awards_number = len(br_temp) + 1


              return awards_number


        else: #'Awards' table row not found
            return 0;





def h3_award_search(soup):
    awards_found = 0
    awards_word = 0

    h3_temp = soup.find_all('h3')
    for h in h3_temp:  # Check if there is the word 'Awards' in a h3 header
        if ('Awards' in str(h)):
            awards_word = 1

    # find all the lists of the html code
    ul_tags = soup.find_all('ul')  # get all the <h3 tags>
    for list in ul_tags:
        # find the <h3> tag before each list
        h3_p = list.find_previous('h3')
        # if the <h3> tag is the Awards tag, the list is the one we want
        if ('Awards' in str(h3_p)):
            awards_list = list
            awards_found = 1
            break

    if (awards_found == 1):
        awards = awards_list.find_all('li')
        return len(awards)

    elif ((awards_found == 0) and (awards_word == 1)):  # 'Awards' found in a h3 header but has no list
        return 'Awards found but cannot be counted'

    elif ((awards_found == 0) and (awards_word == 0)):  # No awards found
        return 0




def h2_award_search(soup):
    awards_found = 0
    awards_word = 0

    h2_temp = soup.find_all('h2')
    for h in h2_temp:      #Check if there is the word 'Awards' in a h2 header
        if ('Awards' in str(h)):
            awards_word = 1



    # find all the lists of the html code
    ul_tags = soup.find_all('ul')  # get all the <h2 tags>
    for list in ul_tags:
        # find the <h2> tag before each list
        h2_p = list.find_previous('h2')
        # if the <h2> tag is the Awards tag, the list is the one we want
        if ('Awards' in str(h2_p)):
            awards_list = list
            awards_found = 1
            break

    if (awards_found == 1):
        awards = awards_list.find_all('li')
        return len(awards)

    elif((awards_found == 0) and (awards_word == 1)):   #'Awards' found in a h2 header but has no list
        return 'Awards found but cannot be counted'

    elif((awards_found == 0) and (awards_word == 0)): #No awards found
        return 0






    #function for extracting the number of awards of a scientist
def extract_awards(soup):


    # First check: check if the awards are contained in a list after a <h2> tag which contains the word "Awards".

    awards_number = h2_award_search(soup)  # number of awards found from the first check
    awards_number1 = 0  # number of awards found from the second check (if the first check failed)
    awards_number2 = 0  # number of awards found from the third check (if both of the previous checks failed)

    # Check if the number of the awards is not found
    if ((awards_number == 0) or (awards_number == 'Awards found but cannot be counted')):
        # Then second check: check if the awards are contained in a list after a <h3> tag which contains the word "Awards".

        awards_number1 = h3_award_search(soup)

        if ((awards_number1 == 0) or (awards_number1 == 'Awards found but cannot be counted')):
            # Then third check: check if the awards are contained in a list in the computer scientist's Wikipedia table.
            awards_number2 = table_award_search(soup)
            if ((awards_number2 == 0) and (awards_number1 == 0) and (awards_number == 0)):
                # awards not found in any of the three searches
                return 0

            elif ((awards_number2 == 0) and ((awards_number == 'Awards found but cannot be counted') or (
                    awards_number1 == 'Awards found but cannot be counted'))):
                return 'Awards found but cannot be counted'
            else:
                return awards_number2  # awards found in the third search


        else:
            # awards found in the second search
            return awards_number1





    # awards found in the first search
    else:
        return awards_number

#function for extracting surname of a scientist
def extract_surname(soup):
    try:  
        temp_html = soup.find('div', class_='mw-content-ltr mw-parser-output') #get each scientist's name
        name = temp_html.find('p', class_='').b

        z = 1

        if name is None:
            while name is None:
                name = temp_html.find_all('p', class_='')
                name = name[z].b
                z = z + 1

        name = name.text
        name = lastWord(name)
        return name
    except Exception as e:
        print(f"Error extracting surname: {e}")
        return "Unknown"

#extract what education every scientist has had from their wikipedia page
def extract_education(soup):
    education = ""
    education_found = False
    headlines = soup.find_all('h2', class_='')  # Get all the headlines of the page
    for headline in headlines:
        span_tag = headline.find('span', class_='mw-headline')
        title=span_tag.get_text().lower()
        if "education" in title:
            # If "education" is found in the headline
            next_tag = headline.find_next('h2')  # Find the next h2 tag after the headline
            # Collect text from <p> and <ul> elements until the next <h2> tag
            elements = headline.find_next_siblings(['p', 'ul'])
            for element in elements:
                # Concatenate the text of <p> and <ul> elements until the next <h2> tag
                if element.name == 'p':
                    education += element.get_text() + "\n"
                elif element.name == 'ul':
                    education += element.get_text(separator='\n') + "\n"
                if element.find_next('h2') == next_tag:
                    education_found=True #we found education so we set it true!
                    break  # Exit loop when the next h2 tag is encountered
            break  # Exit the loop after processing the education section

    if not education_found:
            alma_mater_label = soup.find('th',class_='infobox-label', string=lambda text: text and "Alma" in text and "mater" in text)
            education_label = soup.find('th',class_='infobox-label', string=lambda text: text and "Education" in text)
            
            label = alma_mater_label or education_label  # Combining both label searches

            if label:
                # Get the corresponding <td> tag containing educational information
                data = label.find_next('td', class_='infobox-data')
                if data:
                    # Extract text from <a> tags inside the <td> element
                    education_list = [a.text for a in data.find_all('a')]

                    # Extract text separated by <br> tags inside the <td> element
                    br_text = data.get_text(separator='\n')
                    if br_text:
                        education_list.extend(br_text.split('\n'))

                    education = ', '.join(education_list)  # Convert list to text
                    education_found=True
  
    if not education_found:
        # Check "Biography", "Life", or "Career" sections
        for headline in soup.find_all('span', class_='mw-headline'):
            title = headline.get_text().lower()
            if "biography" in title or "life" in title or "career" in title:
                paragraph = headline.parent.find_next('p')
                if paragraph:
                    education += paragraph.get_text() + "\n"
                    education_found = True
                    break

    if not education_found:
        # Get the first and second <p> tags on the page
        paragraphs = soup.find_all('p')
        for p in paragraphs[:2]:
            next_tag = p.find_next('h2')
            education += p.get_text() + "\n"
            if p.find_next('h2') == next_tag:
                education_found = True
                break

    return education


#asynchronous function for fetching information about scientists
async def fetch_info(session, link):
        async with session.get(link) as response:
            if response.status == 200:
                html_text = await response.text()
                soup = BeautifulSoup(html_text, 'lxml')
                
                    
                # Return a dictionary with extracted information
                return {
                    'surname': extract_surname(soup),
                    'awards': extract_awards(soup),
                    'education': extract_education(soup),
                               }
            else:
                return None

async def main():
    href_obj = []  #a list where the hrefs will be stored
    scientist_info_list = []  #a list where the surnames of the computer scientists' pages will be stored
    links = []  #a list where the links of the computer scientists' pages will be stored
    names_list = []  #a list to store names

    async with aiohttp.ClientSession() as session:
        html_text = await session.get('https://en.wikipedia.org/wiki/List_of_computer_scientists')
        soup = BeautifulSoup(await html_text.text(), 'lxml')
        list_items = soup.find_all('li', class_='') #get the <li>s that have no class

        for l in list_items:        #for each <li> tag
            a_tag = l.find('a')     #find the first <a> tag
            if a_tag is not None:           #if <a> tag exists
                a_tag_href = a_tag['href']  #get the href (link) of the <a> tag
                href_obj.append(a_tag_href) #add the href in the list
                names_list.append(a_tag.get_text())# Append whole name to the names_list
            else:
                a_tag_text = None

        del href_obj[689:]   #delete the hrefs that don't refer to computer scientists

        #we store the links of the computer scientists' pages in the "links" list
        links = ["https://en.wikipedia.org" + str(h) for h in href_obj]

        tasks = []
        for link in links:      #visiting each scientist's page
            tasks.append(fetch_info(session, link))

        scientist_info_list = await asyncio.gather(*tasks)

        #Changing some elements in the surname list, because some surnames have peculiarities
        scientist_info_list[24]['surname'] = 'Bachman'
        scientist_info_list[26]['surname'] = 'Backus'
        scientist_info_list[33]['surname'] = 'Bauer'
        scientist_info_list[44]['surname'] = 'Blaauw'
        scientist_info_list[62]['surname'] = 'Bourne'
        scientist_info_list[63]['surname'] = 'Bouwman'
        scientist_info_list[71]['surname'] = 'Brinch Hansen'
        scientist_info_list[73]['surname'] = 'Brooks'
        scientist_info_list[77]['surname'] = 'Caballero Gil'
        scientist_info_list[84]['surname'] = 'Carmack'
        scientist_info_list[96]['surname'] = 'Clarke'
        scientist_info_list[98]['surname'] = 'Codd'
        scientist_info_list[110]['surname'] = 'Corbató'
        scientist_info_list[142]['surname'] = 'Dix'
        scientist_info_list[146]['surname'] = 'Draper'
        scientist_info_list[154]['surname'] = 'Eckert'
        scientist_info_list[158]['surname'] = 'Emerson'
        scientist_info_list[181]['surname'] = 'Ford' #Ford Jr. 
        scientist_info_list[180]['surname'] = 'Forbus'
        scientist_info_list[201]['surname'] = 'Gates'
        scientist_info_list[204]['surname'] = 'Geschke'
        scientist_info_list[257]['surname'] = 'Hehner'
        scientist_info_list[288]['surname'] = 'Ingalls'
        scientist_info_list[335]['surname'] = 'Kruskal'
        scientist_info_list[405]['surname'] = 'Moore'
        scientist_info_list[475]['surname'] = 'Pieraccini'
        scientist_info_list[511]['surname'] = 'Royce'
        scientist_info_list[568]['surname'] = 'Steele'

         #Setting the number of awards for some scientists, because we could not fetch the number from their wikipedia page with the web crawler

        scientist_info_list[50]['awards'] = 12
        scientist_info_list[58]['awards'] = 8
        scientist_info_list[92]['awards'] = 7
        scientist_info_list[145]['awards'] = 5
        scientist_info_list[191]['awards'] = 9
        scientist_info_list[238]['awards'] = 2
        scientist_info_list[268]['awards'] = 7
        scientist_info_list[286]['awards'] = 3
        scientist_info_list[313]['awards'] = 6
        scientist_info_list[370]['awards'] = 2
        scientist_info_list[387]['awards'] = 3
        scientist_info_list[393]['awards'] = 10
        scientist_info_list[400]['awards'] = 7
        scientist_info_list[422]['awards'] = 2
        scientist_info_list[434]['awards'] = 1
        scientist_info_list[441]['awards'] = 7
        scientist_info_list[486]['awards'] = 11
        scientist_info_list[488]['awards'] = 5
        scientist_info_list[501]['awards'] = 5
        scientist_info_list[514]['awards'] = 3
        scientist_info_list[516]['awards'] = 1
        scientist_info_list[545]['awards'] = 10
        scientist_info_list[577]['awards'] = 5
        scientist_info_list[586]['awards'] = 4
        scientist_info_list[607]['awards'] = 13
        scientist_info_list[609]['awards'] = 8
        scientist_info_list[636]['awards'] = 2
        scientist_info_list[669]['awards'] = 1

        # Saving scientist info to JSON file
        with open("scientist_info.json", "w", encoding='utf-8') as outfile:
            json.dump(scientist_info_list, outfile, indent=3,ensure_ascii=False)
            #with ensure_ascii=False, non-ASCII characters are represented directly in the JSON file without escaping them as Unicode escape sequences.
        






asyncio.run(main())

# Report

## Abstract

<p> This document is a report for the final project of CS582 (Information Retrieval)
 at The University of Illinois at Chicago. The project involved develpoing a 
 web search-engine from scratch for the UIC domain. The software was built using Python3
 and Django(open-source web framework). Different django apps were created to make 
 the code modular.</p>
 
 <p>
 We were also required to add an intelligent feature to the search engine. For the 
 intelligent feature aspect I added 'relevance feedback' and 'pseudo relevance feedback'.
 This was expected to make these improvements to the search engine: </p>
 
 * Not focusing all the results on just the words in the query, but include content
 related to the retrieved set of pages using the query.
 * Expanding the list of results to results that may not contain any word from the
 query but can still be of interest and as it might relate to the same topic.
 * Helping user generate a better query using his feedback on relevant and 
 non-relevant results.  
 
 [Github Link](https://github.com/saurabhsangwan/IR-Search-Engine)
 Note- Github will not contain the database file and pre-built indexes because of size limit.
 
 ---
 ---
 ## 1. Software Description
 
 ###1.1 Introduction
 <p>The software is written in Django(python web-framework) following Object Oriented
 Design Principles. To make it easy to use and test without performing extensive time consuming
 tasks like crawling and pre-processing, I have included the database
 and index files in the code itself. The dataset contains 7800 documents/web-pages
 crawled from the UIC domain. You can start the project simply by installing dependencies
 and using the command 'python manage.py runserver'. You can also run the commands to
 crawl the database and create the index using django-shell(explained in ReadMe file).
 
 ###1.2 Storage
 <p> I have used two types of storage to store the indexes and craweled data - 
 
 * SQLite - It is a simple file based relational database management system (RDBMS) contained in a C library. 
 I have used it to store crawled data in the from of url and text content.
 
 * pickle - 
The pickle module implements binary protocols for serializing and de-serializing a Python object structure.
It is used to store the inverted index and document indexes in a file. The file is read 
when the program initiates and loads the indexes into the main memory. 
 </p>
 
 ###1.3 Crawling
 <p>To perfrom crawling you first have to enter the django shell. The command for this is 
 "python manage.py shell" from the project directory.
 Once you enter the shell run the following code - </p>
 
 ~~~
from crawler.WebCrawler import WebCrawler
s = WebCrawler("https://cs.uic.edu")
s.run_scraper()
 ~~~
 
 <p>This starts crawling from the page - 'https://cs.uic.edu'. The crawler used multi-threading to crawl through 
 the web pages. It uses a breadth first stategy, where every page is first dequeued and processed,
 its data is extracted and updated in the database. The links from this page are then extracted, validated (
 checked if they belong to the UIC domain - 'https://www.uic.edu/')  
 and enqueued to a FIFO queue. Validation also includes checking of possible bad extensions
  like "pdf", "jpg", "jpeg", "doc", etc.. Connection timeout was defined as connect timeout and read timeout 3 and 60 
  seconds respectively, so that the threads dont get blocked. </p>
  
  <p>
  The urls are also preprocessed before being added to the queue, all the 'http' urls are converted
  to 'https'. All the urls are ensured to end with a '/'. After pre-processing, the url is checked 
  if it has already been crawled by comparing it with a set of already crawled urls and is then added to the queue.  
  </p>
  <p>
  A primary key 'id' is associated with each document in the database and is used to uniquely
  identify each document and its content.
  </p>
  
###1.4 Pre-processing
<p> The pre-processing of the crawled data can be executed similary from the django-shell using the 
following code-snippet - </p>

~~~
from vectorise.utils import create_index
create_index()
~~~

<p>In the pre-processing part we create an inverted index, and document indexes to store data like tf, idf scores.
This also includes tasks like stop word removal and stemming.
The data is stored in a binary file using pickle module of python. This data is read when the 
application is started to load the indexes in memory.</p>

### 1.5 User Interace
<p> I implemented a simple user interface using HTML and CSS. </p>

* Home Page - The home page is very simple and intuitive to use. You type your
query in the Search(text) box and then click on the search button.
![Home Page](/home/saurabh/Pictures/Screenshot from 2020-05-02 23-23-21.png)

* Results Page - The result page is also simple and intuitive. In the image below, you 
can see the results for query - 'cornelia'. There is a radio button next to each result, 
to mark it as relevant and not relevant. After making such choice, the user can click on 
the submit button to improve the search query. Also, there is a box next to the search button
titled - 'No. of Results:', this can be used to limit or increase the maximum number of resutls
to be returned for a particular query. 10 is the default number for this field.
![Results Page](/home/saurabh/Pictures/Screenshot from 2020-05-02 23-31-33.png)

### 1.6 Querying and Retrieving

* Pseudo Relevance Feedback - 
The query string is first tokenised and stemmed, then it is used to retrieve a list of documents
based on the cosine similarity. The top 30 ranked documents from these documents are then 
processed to find words with highest cummulative tf-idf weigths across these documents, top five words based on the weight,
are then added to the original query ensuring it does not add duplicates to the query.
This new query is then used to retrieve the final result of ranked documents. By default only top 10
results are shown to the user.

* Relevance Feedback - 
Once the user submits the relevant and not relevant documents from the results page.
We calculated the top five words(based on cummulative tf-idf weight across these documents), 
for both sets of documents. The words from the non-relevant set are removed from the original query
and those from the relevant set are added to the query ensuring it doesn't add duplicates to form
the new query string. This new query string is not used to retrieve documents for the user.

---

## 2 Main Challenges

The main challenges I encountered while working on this project are - 

* Initially it was very hard to fix upon the smart components I wanted to include in the 
project. With little experience working on such projects, and thinking on improvements 
without having a working demo, was a hard decision to make.

* While implementing I challenged myself to work on different technologies and modules, the ones
I thought were best suited for the project. I wanted it to be a web application, so I had to learn
some new technologies like Django, HTML for that. Also, I had to learn how to use multi-threading 
in python for the crawler, so it does not end up taking a lot of time.

* There were a lot of things I learned by trial and error during the development process. E.g. 
Ensuring no duplication of urls while crawling, like some urls had 'http' while some had 'https', 
also some had a trailing '/' in the end and some did not. But they were essentially pointing to the 
same document. Also, I had to skip urls ending up in a bad format like "pdf", "jpg", "jpeg", "doc", etc.

* Another challenging thing, was defining the value of parameters like number of documents to be
considered for pseduo relevance feedback, what number of top weighted words to consider, etc.
I compared the results for different values and then picked the ones that worked best.

## 3 Weighting Scheme and Similarity Measure

* Weighting Scheme - The weighting scheme that I used was 'tf–idf'. It is a widely used numerical
 statistic that is intended to reflect how important a word is to a document in a collection or corpus.
 The tf–idf value increases proportionally to the number of times a word appears in the document and 
 is offset by the number of documents in the corpus that contain the word, which helps to adjust for 
 the fact that some words appear more frequently in general. It is better than alternatives which use just
 'tf' and not 'idf' since they fail to comprehend the importance to the word in terms of the entire 
 dataset. 
 
* Similarity Measure - I used cosine similarity measure to rank documents. I used this method
over inner product as cosine similarity only cares about the angle difference between the query and
the document vector in the vector space whereas inner product cares about both the 
angle and the magnitude. Since, our data was not normalised on the length of documents,
I wanted the length of documents to not be a factor when calculating similarity and found
it desirable to ignore the magnitude.

## 4 Intelligent Components 
<p> I wanted to add features to expand the result of a query, as I believe query formulation
is one of the most challenging tasks in an IR system. The user does not always know what 
 exactly he is looking for and how to formulate the query. A simple static query expansion
  based on synonyms seemed too simplistic and would not have done well to capture semantic concept.
  Intending to solve this problem I 
 implemented two smart components in my project.</p>

* Pseudo Relevance Feedback - also known as blind feedback. In this we take top k-ranked documents
from the retrieved documents(assuming they are relevant), and use these documents to further 
expand the query and retrieve more documents. To extract words to expand the original query,
I used the tokens with the highest tf-idf value in the document, I also used the cummulative sum
of these values across the original documents to then retrieve top n such words. These words are then
added to the original query avoiding duplicates. This functionality is flag-based, and can be turned 
off by changing the value in the settings file.

* Relevance Feedback - I also thought that the results could be better if the user can tell us what
documents are more relevant to his context. For this I implemented relevance feedback. The user
can select the relevant and non-relevant documents from the initial result(which includes query expansion using
pseudo relevance feedback). Now from this we perform a process similar to the pseudo-relevance 
feedback, we remove top n-words from the non-relevant set of documents from the query and add the ones
from the relevant set of documents to the query, in this order avoiding duplicates.

## 5. Evaluation 

1 Query - "Cornelia"

* Pseudo Relevance Feedback - 
The results inluded links to the professor's(Cornelia Caragea, PhD) profile page, while also
including links to the all professors(CS Dept.) TA hours, an article welcoming her to UIC, profile pages 
of professors with similar research interests(Shanon Reckinger and Evan McCarty), and a couple of articles
about UIC projects and grants received in such areas. All the results were relevant. (Precison - 1.0)
* Relevance Feedback - After marking the profile page of Prof Shanon Reckinger as non relevant, we get a list 
of only four pages. The profile page of professor's(Cornelia Caragea, PhD), Office hours page and articles mentioning her.
All the results are considered relevant. (Precision - 1.0)

2. Query - "jobs and internship"
* Pseudo Relevance Feedback - All the results included references to internship and job programs at Engineering Career Center,
we consider all these as relevant. (Precision -1.0)
* Relevance Feedback - After marking and internship result as irrelevant, we are only left with links
containing job references mostly from "jobs.uic.edu" and some from individual departments job postings page like
"Academic Computing and Communications Center"(https://accc.uic.edu/jobs/). All results were relevant.
(Precision -1.0)

3. Query "compute science admission"
* Pseudo Relevance Feedback - Relevant results included references to "cs.uic.edu" graduate and undergraduate 
admisson's pages, and faq pages(count 8). Non-relevant results included references to "https://admissions.uic.edu/"
contact page and undergraduate admissons page(count 2). (Precision - 0.8)
* Relevance Feedback - After marking the non-relevant pages as such. The relevant results included the 
earlier references to relevant pages(count-6). The changed results included references to Computer Science
Department Calendar and profiles of some faculty(Non relevant, count-4). (Precision - 0.6)

4. Query - "career fair"
* Pseudo Relevance Feedback - Relevant results includes links to "ecc.uic.edu" career and career fair pages, 
and "careerservices.edu" career fair page(count 7). Non relevant results included - links to LinkedIn 
workshop, alumni pages(count 3). (Precision - 0.7)
* Relevance Feedback - On marking the "https://ecc.uic.edu/engineering-career-fair/" page as relevant, the results
did not change. (Precision - 0.7)

5. Query - "scholarship"
* Pseudo Relevance Feedback - Relevant results included links to Office of International Affair's funding opportunites, sources, and
scholarship results. They also included results from "https://scholarships.uic.edu/" external scholarship page(Count 8).
Non Relevant Results included results from "give.uic.edu" which was about donating money to funds and scholarships, not
relevant in the user context(Count-2). (Precision - 0.8) 
* Relevance Feedback - On marking the "https://scholarships.uic.edu/scholarships/external-scholarships/" page as relevant.
The results were all relevant to the query including further links from "SnAP" - Scholarship and Awards Program and "studyabroad.uic".
(Precision - 1.0)

## 6. Results

Based on the original query the intelligent components were able to make some improvements. 
* Pseudo Relevance Feedback was always able to expand the set of retrieved documents. This worked really 
well when the original query could find only find a small set of documents. E.g. Query 'cornelia' could originally 
fetch only 4 documents. 

* From this expanded set, I was better able to narrow down my results(by formulating a better query) using Relevance Feedback by marking
the relevant and non-relevant results as such. 

Things that did not work - 
* Using Pseudo Relevance Feedback, sometimes the best results were not the top ranked documents,
this happened because of query expansion and reduced weight of the original query terms. 

## 7. Related Work

<p>Query Expansion Strategy based on Pseudo Relevance Feedback and Term Weight Scheme for Monolingual Retrieval - Rekha Vaidyanathan, Sujoy Das, Namita Srivastava</p>
In the paper they proposed a method for query expansion. The proposed method tries to extract
keywords that are closer to the central theme of the document.
The expansion terms are obtained by equi-frequency partition
of the documents obtained from pseudo relevance feedback
and by using tf-idf scores. The idf factor is calculated for
number of partitions in documents. The group of words for
query expansion is selected using the following approaches:
the highest score, average score and a group of words that has
maximum number of keywords.</p>
<p>
I have implemented a simpler version of this for query expansion for both pseduo-relevance feedback and relevance feedback.
I have used tf-idf alone to identify the top words of a document as representatives of the 
document-data. In pseudo relevance feedback I have also assumed that the first k-documents retrieved are all correct.</p>


## 8. Future Work
<p>Due to the lack of labelled data, its hard to evaluate the results. Things that can be improved 
in future are - 

* Parameter Tuning - The number of documents are words to be used for relevance feedback can be further 
tuned with the help of comprehensive evaluation of results using labelled data.

* Different weights for expanded query tokens- Currently, there is no provision to provide different
scores for the expanded tokens in the query, this weight of scores can be added and further tuned to provide better results as well.
</p>
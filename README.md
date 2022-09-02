# WikipediaSearchEngine
## A scalable and efficient search engine on wikipedia pages

### Projective: Project Objective
- In this project, the task was to build a scalable and efficient search engine on Wikipedia pages. This constituted two stages - inverted index creation and query search mechanism, where the scope of performance in the second stage relied heavily on the quality of index built in its preceding stage. Throughout the project, efforts were been made to build a system optimized for search time, search efficiency (i.e. the quality of results), indexing time and index size. We have used Wikipedia dumps of size over 90 GB in XML format, which is parsed to get Wikipedia pages.

---
### Directory Structure
- **filehandler.py**
- **indexer.py**
- **merger.py**
- **search.py**
- **index.sh**
- **invertedindex_stats.txt**
- **README.md (duh)**
---
### Optimizations Used
- XML parser was used over the DOM Parser since in SAX, we never load the full xml file into the RAM, but only pieces we need in the moment, whereas in DOM - document object model, we load the entire xml file into RAM and create hierarchical structure.
- Used a stemmer over a lemmatizer for better performance.
- Symbols like curly braces and angular braces, along with html tags were removed.
- Hyperlinks were substituted with the empty string.
- The Min-Heap method was used to merge K sorted index files.
- File size was limited to 15000 terms per indexfile.
- After the creation of the primary index, a secondary index was created to further facilitate smoother search.
- The length for each term was restricted to 2-35.
- Title was given priority in ranked retrieval.
- Time and Space are effectively inversely proportional to each other. The more expressions we remove from the index creation to reduce the size, the more time it takes. Efforts were made to find a balance between the two.
- For the smaller dataset ~ 1.6GB:
    - Index Size ~ 328 MB
    - Index Creation Time ~ 310 Seconds
- The index format is defined below:
```
amand:d317970b1
amanda:d317994b1l1 d318090b1 d318624b89 d318732b1 d318791b1 d318879b1 d320357b2 d321347b1 d324331b2 d324436b1l1 d325018b1 d325025b1 d325596b1 d325891b2 d327309b3 d329562b1
```
- **d** represents the document number/id.

- Support is offered for both plain & field queries.

- The number after each of these symbols denote the count of terms in that particular section in that particular document.

    | FIELD | Title | Info | Category | Body | References | External Links |
    | ------ | ------ |------ | ------ |------ | ------ |------ | 
    | **SYMBOL** | t | i | c | b | r | l |

---
### **How to run**
### Index Creation
For creating indexes use the following command : 
```
bash index.sh <path to data> <path to dir to store the index> <invertedindex_stats.txt>
```

### Merging the index to create primary and secondary index
Once the index files have been created, we need to merge them into one large file by using the algorithm to merge k-sorted arrays using a min-heap. The code creates two folders, "primary" which contains the primary index and "secondary" which contains the files for the secondary index.

To merge the index, run:
```
python3 merger.py
```

### Query Search
For each query string, it returns the top 10 results, each result consisting of the document id and title of the page. 
The output is stored in the queries_op.txt file, which displays top 10 results along with the time taken to process the query.
The queries will be provided in a `queries.txt` file. It can be run as: 

```
python3 search.py queries.txt queries_op.txt
```


---
### Points to note:
- Difficult to process large data of 90 GB. Had to resort to using ada for the same.
- Can not store word & its posting list directly into main memory, so was necessary to use minheap to sort sorted lists.
- Due to its size, we cannot Load the full final index into main memory, So it was necessary to build a Secondary Index on top of the Primary Index.
---

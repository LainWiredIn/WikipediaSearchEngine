# Search Engine Knowledge

1. XML: What is it?

- Extensible Markup Language
- text-based format for structuring and sharing data across networks, between programs and between people.
- Despite its similarity to HTML which is also based on SGML standards, the XML format adheres to the strict formatting rules.
- Furthermore, XML is more predictable and readable making it easier to spot and resolve errors.
- While virtually all tags used in HTML are predefined, XML tags on the other hand are not, making it even more extensible.

2. Structure of XML documents

- All XML documents must have a root element which is considered as the parent element of all other elements.
- Most XML elements also contain an optional prolog. However if the prolog element exists within an XML document, then it must be in the first line in the XML document.
- The XML prolog mat is used to specify a character encoding for XML documents which are often UTF-8, versioning and other international characters.
- It is illegal to omit a closing tag in an XML document. However, the Prolog tag is not considered as part of the XML document and is, therefore, an exception to this rule.
- Tags in XML documents are case sensitive, cases used in opening tags must match those of their counterparts, the closing tags.
- XML elements can also have attributes with their corresponding attribute values, in such instances attribute values should always be kept in quotes.

3. Tokenization

- https://goodboychan.github.io/python/datacamp/natural_language_processing/2020/07/15/01-Regular-expressions-and-word-tokenization.html#Practicing-regular-expressions---re.split()-and-re.findall()

4. Stemmer

- https://www.projectpro.io/recipes/use-porter-stemmer
- https://www.analyticsvidhya.com/blog/2022/06/stemming-vs-lemmatization-in-nlp-must-know-differences/#:~:text=Stemming%20is%20a%20process%20that,'%20would%20return%20'Car'.
- https://www.geeksforgeeks.org/nlp-how-tokenizing-text-sentence-words-works/#:~:text=Tokenization%20is%20the%20process%20of,Sentences%20into%20words%20tokenization
- https://towardsdatascience.com/5-simple-ways-to-tokenize-text-in-python-92c6804edfc4#31ad
- https://goodboychan.github.io/python/datacamp/natural_language_processing/2020/07/15/01-Regular-expressions-and-word-tokenization.html#Practicing-regular-expressions---re.split()-and-re.findall()

5. Term Frequency

- Thus far, scoring has hinged on whether or not a query term is present in a zone within a document. We take the next logical step: a document or zone that mentions a query term more often has more to do with that query and therefore should receive a higher score. To motivate this, we recall the notion of a free text query introduced in Section 1.4 : a query in which the terms of the query are typed freeform into the search interface, without any connecting search operators (such as Boolean operators). This query style, which is extremely popular on the web, views the query as simply a set of words. A plausible scoring mechanism then is to compute a score that is the sum, over the query terms, of the match scores between each query term and the document.

- Towards this end, we assign to each term in a document a weight for that term, that depends on the number of occurrences of the term in the document. We would like to compute a score between a query term $t$ and a document $d$, based on the weight of $t$ in $d$. The simplest approach is to assign the weight to be equal to the number of occurrences of term $t$ in document $d$. This weighting scheme is referred to as term frequency and is denoted $\mbox{tf}_{t,d}$, with the subscripts denoting the term and the document in order.

- For a document $d$, the set of weights determined by the $\mbox{tf}$ weights above (or indeed any weighting function that maps the number of occurrences of $t$ in $d$ to a positive real value) may be viewed as a quantitative digest of that document. In this view of a document, known in the literature as the bag of words model , the exact ordering of the terms in a document is ignored but the number of occurrences of each term is material (in contrast to Boolean retrieval). We only retain information on the number of occurrences of each term. Thus, the document ``Mary is quicker than John'' is, in this view, identical to the document ``John is quicker than Mary''. Nevertheless, it seems intuitive that two documents with similar bag of words representations are similar in content. We will develop this intuition further in Section 6.3 .

- Before doing so we first study the question: are all words in a document equally important? Clearly not; in Section 2.2.2 (page [*]) we looked at the idea of stop words - words that we decide not to index at all, and therefore do not contribute in any way to retrieval and scoring. 

6. Inverse Document Frequency

- https://nlp.stanford.edu/IR-book/html/htmledition/inverse-document-frequency-1.html

7. Combining the two

- https://nlp.stanford.edu/IR-book/html/htmledition/tf-idf-weighting-1.html
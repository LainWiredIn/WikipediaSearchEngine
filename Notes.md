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

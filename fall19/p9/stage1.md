# Stage 1

For the first few questions, we'll ask you to list files.  These
questions have a few things in common:
* any files with names beginning with "." should be excluded
* you must produce a list
* the list must be in reverse-alphabetical order

Some things will vary:
* which directory you'll look at
* whether the list contains simples file names, or paths
* sometimes you'll need to filter to only show files with certain extensions

You may consider writing a single function to answer several questions
(hint: things that change for different questions can often be
represented with parameters).

----

#### Question 1: What are the names of the files present in the `data` directory?

Hint: Look into the  `os.listdir`  function. Produce a list of file names, sorted in  **reverse-alphabetical**  order.

#### Question 2: What are the paths of all the files in the `data` directory?

In order to achieve this, you need to use the `os.path.join()`
function. Please do not hardcode "/" or "\\" because doing so will
cause your function to fail on a computer that's not using the same
operating system as yours.

#### Question 3: What are the paths of all the CSV files present in `data` directory?

Filter to only include files ending in `.csv`

#### Question 4: What are the paths of all the files present in `data` directory, that begin with the phrase `'review'`?

----

We will first try to read the JSON file `products.json`. You might find it useful here, to create a function to read JSON files.

#### Question 5: What are the products in `products.json`?

Your output should look like this:
```python
{'B00QFQRELG': 'Amazon 9W PowerFast Official OEM USB Charger and Power Adapter for Fire Tablets and Kindle eReaders',
 'B01BH83OOM': 'Amazon Tap Smart Assistant Alexa enabled (black) Brand New',
 'B00ZV9PXP2': 'All-New Kindle E-reader - Black, 6" Glare-Free Touchscreen Display, Wi-Fi - Includes Special Offers',
 'B0751RGYJV': 'Amazon Echo (2nd Generation) Smart Assistant Oak Finish Priority Shipping',
 'B00IOY8XWQ': 'Kindle Voyage E-reader, 6 High-Resolution Display (300 ppi) with Adaptive Built-in Light, PagePress Sensors, Wi-Fi - Includes Special Offers',
 'B0752151W6': 'All-new Echo (2nd Generation) with improved sound, powered by Dolby, and a new design Walnut Finish',
 'B018Y226XO': 'Fire Kids Edition Tablet, 7 Display, Wi-Fi, 16 GB, Pink Kid-Proof Case',
 'B01ACEKAJY': 'All-New Fire HD 8 Tablet, 8 HD Display, Wi-Fi, 32 GB - Includes Special Offers, Black',
 'B01AHB9CYG': 'All-New Fire HD 8 Tablet, 8 HD Display, Wi-Fi, 32 GB - Includes Special Offers, Magenta',
 'B01AHB9CN2': 'All-New Fire HD 8 Tablet, 8 HD Display, Wi-Fi, 16 GB - Includes Special Offers, Magenta',
 'B00VINDBJK': 'Kindle Oasis E-reader with Leather Charging Cover - Merlot, 6 High-Resolution Display (300 ppi), Wi-Fi - Includes Special Offers',
 'B01AHB9C1E': 'Fire HD 8 Tablet with Alexa, 8 HD Display, 32 GB, Tangerine - with Special Offers',
 'B018Y229OU': 'Fire Tablet, 7 Display, Wi-Fi, 8 GB - Includes Special Offers, Magenta'}
```

The keys in the above dictionary are the Amazon Standard Identification Numbers (or asin), that Amazon uses to identify its products.

We will now try to read the CSV files that contain the reviews. Once again, you should consider creating a function to read CSV files given the filename. Use this function to read `review1.csv` to see what's in there.

#### Question 6: What is the review *text* of review with id `1410`?

#### Question 7: What is the review *text* of review with id `69899`?

Careful, this one isn't in `review1.csv`. To get credit, make sure
your code looks through all the CSV files to find the review.

#### Question 8: What is the review *title* of review id `28013`?

#### Question 9: What file contained the review with that id?

----

Note that the CSV files we have been reading so far do not contain any information about the product that is being reviewed! That information is stored in the JSON files.

Each JSON file stores information about the reviews in the corresponding CSV file. So, `review1.json` stores information about the reviews in `review1.csv`, `review2.json` stores information about the reviews in `review2.csv` and so on. Feel free to take a look at any of these JSON files, to see how the data is stored.

----

#### Question 10: What is the data stored in `sample_reviews.json`?

`sample_reviews.json` contains a subset of the information in `review1.json`. Your output should look like this:
```python
{'10101': ['Mikey123456789', 'B00QFQRELG'],
 '99904': ['diamond', 'B00QFQRELG'],
 '89604': ['Pat91', 'B00QFQRELG'],
 '58704': ['Frank', 'B00QFQRELG'],
 '38104': ['LADYD92', 'B00QFQRELG']}
```

The keys are the review ids, and the value stored is a list, containing the name of the user who made the review, as well as the asin of the reviewed product.

----

As we can see, the review data is distributed between different files. It would be useful to combine this data.

For the following questions, you'll need to create a new Review type
(using namedtuple).  It should have the following attributes:

* id (int)
* username (string)
* asin (string)
* title (string)
* text (string)
* rating (int)
* do_recommend (bool)
* num_helpful (int)
* date (string)

Please ensure you define your namedtuple exactly according to the
specifications above, or you will be unable to pass the tests.  You
should be able to use your Review type to create new Review objects, like this:

```python
review = Review(68358, "Preacherman", "B01BH83OOM", "Easy to set up" , "Enjoying the product and feel the ease of use is good.", 5, True, 0, "2017-07-07")
review
```

Running the above in a cell should produce output like this:

```
Review(id=68358, username='Preacherman', asin='B01BH83OOM', title='Easy to set up', text='Enjoying the product and feel the ease of use is good.', rating=5, do_recommend=True, num_helpful=0, date='2017-07-07')
```

----

Build a function `get_reviews` that accepts a CSV review file and a JSON review file and combines them to produce a list of `Review` objects, which it either returns or yields (your choice!).

#### Question 11: What is produced by your function `get_reviews('sample_reviews.csv', 'sample_reviews.json')`?

The output should be a list of five Reviews.  If you chose to write a generator with yield, just convert the generator object to a list.

Be careful, if you get the types wrong for any of the Reviews, the tests won't recognize it.

#### Question 12: What are the first ten Review objects in the list produced by `get_reviews('review1.csv', 'review1.json')`?

#### Question 13: What are the last ten Review objects in the list produced by `get_reviews('review2.csv', 'review2.json')`?

It is likely that your code crashed or your output has some missing data. That is because some of the rows in the CSV files are incomplete. Go back and modify the function you used to parse the CSV file, so that any rows that have missing data are ignored.

In other words, if any row in a CSV file does not have all its fields, the row should be skipped entirely.

#### Question 14: What is the Review object with review id `84713`?

#### Question 15: What is the Review object with review id `42931`?

#### Question 16: List the first ten Review objects in the entire dataset, sorted by increasing order of their review ids.

It is likely that your code crashed when you tried to read some of the files. That is because some of the JSON files are broken. Unlike broken CSV files, broken JSON files are much harder to salvage. Your code should skip any JSON files that you are unable to parse using  `json.load`.

----

For this last section, we will now try to combine the data we have stored in the Review objects with the data from `products.json`.

#### Question 17: Output the number of review objects for the product, "Amazon Tap Smart Assistant Alexa enabled (black) Brand New".

#### Question 18: Output the number of review objects for the product, "All-New Fire HD 8 Tablet, 8 HD Display, Wi-Fi, 32 GB - Includes Special Offers, Black".

#### Question 19: Find the name of the product with most reviews.

#### Question 20: Find the most helpful review(s) of this product.

That's it for Stage 1. In the next stage, we'll begin using the data
structures we've set up to do some analysis that spans across multiple
files!

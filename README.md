# Phishing URL Detection Extension:Detect whether a URL is Phishing or Legitimate
### PROCESS OF PROJECT IMPLEMENTATION STEPS

#### I. Cleaning and removing redundant columns of Datasets:
-	Read a CSV file including datasets
-	Remove all columns that don't have labels 0 or 1
-   Remove columns that we don't use (included about 12 columns)

II.	Extract to meaningful columns for training: (Total 22 Features)
1.	Domain: The path of a website
2.	Label: include 0 and 1, 0 is Legitimate and 1 is Phishing
3.	Registered_domain: This is the domain name registered
4.	Url_len: The length of a URL
5.  The 13 next columns are a number of special symbols in a URL such as ~, !, @, #, $, &, ^, *, /, //, ..
6.	Abnormal_url: Check whether a URL is abnormal (1: Yes, 0: No)
7.	https: Check whether a URL has an HTTPS protocol or not (1: Yes, 0: No)
8.	digits: Number of digits in a URL
9.	letters: Number of letters in a URL
10.	shortening_service: Check whether a URL has a shortening service or not (1: Yes, 0: No)
11.	having_ip_address: Check whether a URL has IP address or not (IPv4, IPv6, ..) (1: Yes, 0: No)

III. Get Extracted Columns to Train some models:
-	Get 22 extracted features and save them to the train.csv file
-   Remove some columns that have letters, labels (domain, label, registered_domain)
-	Assuming that X is the data of 22 columns and y is the data of labels 
-	Transmits 2 variables X, y, and the name of the machine learning model (DecisionTreeClassifier, RandomForestClassifier, SVC, …)
-   Perform fitting data followed to corresponding columns	
-	Training Data and save a file has suffix which is .model

IV. Predict the label of any URL by Trained models:
-	Load trained model data
-   From the URL, we extract 22 corresponding features with trained data
-	Remove 2 unused columns (domain, registered_domain)
-   Fit columns with the scope of trained data
-   Predict the label for this URL

V.	Consequent:
-   The result will be Phishing or Legitimate
-   If the result is Phishing:

![alt text](./templates/images/Phishing%20Ressult.png)

-   If the result is Legitimate:

![alt text](./templates/images/Legitimate%20Result.png)

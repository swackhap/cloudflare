# Bulk BIND File Import

Create a zone and upload the corresponding BIND file for each domain based on the corresponding `.txt` file within a directory.
---

Some DNS providers allow you to download all of your zone files as a ZIP folder. Within this folder are text based BIND files which usually follow a strict naming scheme.

That being said, some providers stray from this, so you will want to visually inspect that all files end in '.txt'.


## Features
---
* Reads from a folder filled with `.txt`-based BIND files with the following naming structure:
  * domain1.com.txt
  * domain2.com.txt
* Creates corresponding empty zone on Cloudflare, skipping auto-population of DNS records.
* Uploads BIND files to corresponding empty zone.


## Example
---

1. domain1.com.txt is found in folder.
2. domain1.com is created on Cloudflare.
3. BIND file `domain.com.txt` is uploaded to domain.com on Cloudflare.



## Usage
---
1. Clone this repository.
2. Drop your folder of BIND files in the root directory of the repository.
3. Navigate to the repository with your command line.
3. Run the following command:
```
python Bulk_BIND_Import.py -email [email] -key [key] 
```
_Optionally, you can also add the `-org` flag to specify that these zones should belong to an organization._
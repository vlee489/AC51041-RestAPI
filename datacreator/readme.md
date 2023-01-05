# Sample Data Generator

This short script takes in a directory of video clips and will generate , thumbnails and descriptions
for all the clips. This is designed for clips to be named `{catergory}{some string of numbers1234}.mp4`.

The description text uses a [Markov Class from 
Agiliq Blog](https://www.agiliq.com/blog/2009/06/generating-pseudo-random-text-with-markov-chains-u/) and uses text from
[Project Gutenberg: My Man Jeeves by P. G. Wodehouse](https://www.gutenberg.org/ebooks/8164) as filler text.

The `data.json` is to be loaded into the `Films` collection on your mongoDB database and the thumbnails and the video to
be uploaded to the S3 compatible storage you're using.
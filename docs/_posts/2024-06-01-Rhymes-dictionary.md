---
layout: post
title: "How I built a rhymes dictionary"
date: 2024-06-01
readable_date: 1st June 2024
author: Armand, the maintainer of Remède
cover: /assets/blog_rimes.png
tags: 
  - News
  - Dev
---

_This article was published on [camarm.dev/blog](https://www.camarm.dev/blog) and [dev.to/camarm](https://dev.to/camarm/how-i-built-a-rhymes-dictionary--3fme)_

Hi and welcome to this new article !

I've been working hard on my mobile dictionary Remède this last month (I released the `1.2.0-beta` version a week ago).

I've added many things but today I will focus on a special functionality.

I've added a **rhymes dictionary** which is completely running on your phone (or any browser) without an internet connection !

## 1. - Find data to build a rhymes database

I've searched for open source projects which had already built a rhymes database so I can re-use their database and adapt it for Remède.

After some searches, I discovered that [Open Lexicon](http://www.lexique.org), a project which provides various open database about words, has enough data to build a rhymes dictionary.

I found the [Drime](https://a3nm.net/git/drime/files.html) project, which uses _Open Lexicon_ database to generate its own rhymes database. With their documentation, I built my own base and added these rows in a new table of the Remède database.

## 2. - How it works ?

If you don't know Remède (you can check it out on [Github](https://github.com/camarm-dev/remede) and leave a star), it uses a **Sqlite database** which is downloaded locally.

Now that I have enough fields about words, how can I build an efficient dictionary ?

First, let's explain how this dictionary is working.

A table `rime` contains rows (one row is equal to one word) with the fields `phon_end`, `word_end` (and more fields like `feminine` or `elide` for particular rhymes...).

So for example, to get the rimes of the word `bonjour`, phoneme `\b$ZuR\`, we will filter all the words whose phoneme finishes with `uR`.

_The requests will look like_
```sql
SELECT word FROM rime WHERE phon_end LIKE '%uR'
```

And you understood the main concept ! Now we can add fields to filter and get more specific results, like in the application.

## 3. Final look

Yes we have a dictionary but not anyone can use it ! You must know Sql to browse it...

I tried to have the simplest and most understandable interface. For the interface, I use Ionic 7 with Vue 3.

I integrate this functionality as following in Remède:


| Description                              | Screenshot                                                                                             |
|------------------------------------------|--------------------------------------------------------------------------------------------------------|
| Searching a word in the rimes dictionary | ![Rimes dictionary](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/1kcrbhhrw81zlopyxp39.png) |
| Browsing rimes                           | ![Browsing](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/pkuujri43t8m7ey4dvoc.png)         |
| Set _syllabes_ filter                    | ![Filter](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/pe1orlg7la6bpdxhw9ho.png)           |

## What's next ?

For the moment, some functionalities are missing and the experience is not perfect... I want to add the possibility to choose the "nature" of the wanted rhymes (verb, noun...) and to enhance word finding experience.

Thank you for reading,

Don't hesitate to try Remède (https://remede.camarm.fr, and let me a message about your experience if you want !)

Have nice code !

Armand, the creator and maintainer of Remède.

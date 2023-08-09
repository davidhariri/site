---
title: YouTube Subscriptions via RSS
date: 2023-08-09 21:36:20.708664+00
tags: rss, focus
description: A quick guide on how to watch YouTube in your RSS reader
---

I subscribe to lots of terrific creators on YouTube, but the site and app have become engineered towards discovery. The algorithm makes it easy to watch much more than only what you subscribe to. I don't have enough self-discipline to always use the site effectively so I thought to see if there is a way to subscribe to a YouTube channel with RSS. There is:

```
https://www.youtube.com/feeds/videos.xml?channel_id={{channel_id}}
```

Unfortunately, YouTube doesn't make these links available anywhere (you have to make them yourself) and there's no way to export all your subscriptions in one go. Apparently there used to be, but it's gone from the [Subscription Management page](https://www.youtube.com/feed/channels). And from this page, you can't even get the `channel_id` that we need to make the links anymore. YouTube has public-facing handles (@3blue1brown) and `channel_id` (UCYO_jab_esuFRV4b17AJtAw). This page's links all use the handle. The `channel_id` _can_ be copied from each channel by navigating to it, then clicking "About", then "Share" and finally "Copy channel ID".

I subscribe to over 250 YouTube channels so getting RSS links for each by doing that would be a questionable use of time.

I did a quick search in the sources panel of my browsers dev tools for `UCYO_jab_esuFRV4b17AJtAw` and noticed that YouTube loads all of the data we need to make a `.opml` RSS file as we scroll to the bottom of the page into the DOM. Yay! We can run the following script in our console to create and download a file that we can then import into our favourite RSS reader.

**Instructions**

1. Navigate to [https://www.youtube.com/feed/channels](https://www.youtube.com/feed/channels)
2. Open your browser's dev tools to the "Sources" page.
3. You should see 'channels (www.youtube.com)' or something similar, click that and you should see the DOM. It should start with '<!DOCTYPE html>'.
4. Scroll to the bottom. Keep scrolling until it has loaded all of your subscriptions.
5. Open the console in the dev tools (if it's not already) and paste this script in and press **return** on your keyboard.

```javascript
var opmlData = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<opml version=\"1.0\">\n<body>\n<outline text=\"YouTube Subscriptions\" title=\"YouTube Subscriptions\">\n" + JSON.stringify(ytInitialData.contents).match(/"channelId":\s*"([^"]+)",\s*"title":\s*{\s*"simpleText":\s*"([^"]+)"\s*}/g).map(match => /"channelId":\s*"([^"]+)"/.exec(match)[1]).map(cid => `<outline type="rss" xmlUrl="https://www.youtube.com/feeds/videos.xml?channel_id=${cid}" />`).join('\n') + "\n</outline>\n</body>\n</opml>";
var blob = new Blob([opmlData], { type: 'text/xml' });
var a = document.createElement('a');
a.href = URL.createObjectURL(blob);
a.download = 'subscriptions.opml';
a.click();
```

_Tested in Safari and Chrome on MacOS_

6. You should get a prompt to allow downloads on the page. Accept it and you should have the .opml file you need for your RSS reader.

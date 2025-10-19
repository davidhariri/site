---
title: Make macOS Faster
description: How I made macOS feel as fast and productive as Linux without leaving the walled garden.
date_published: 2025-10-19
tags:
    - guides
    - productivity
    - Apple
    - focus
---

Lately there's been (deserved) hype around DHH's linux flavor Omarchy[^1]. The main benefit? Speed. The closer I can get to using a computer at the speed of thought the better. And I admit to feeling tempted to end my ~30 year romance with macOS and pick up a Framework[^2] and dive in. Or follow the Asahi Omarchy[^3] guides so I can keep my hardware looking nice. But learning a new OS and messing with compatibility issues is just not the stage of life I'm in. 

Thankfully, I'm glad to report that with three awesome pieces of software and a few simple tweaks, I have macOS working and feeling very similarly to Omarchy, without having to boot Linux. Here's how:

<div class="step" data-num="1">Hide the Dock & Menu Bar</div>

1. Open <a class="quick_link" href="x-apple.systempreferences:com.apple.Desktop-Settings.extension">Dock Settings</a> (System Settings -> Desktop & Dock) and turn on 'Automatically hide and show the Dock'

2. Open <a class="quick_link" href="x-apple.systempreferences:com.apple.preference.dock">Menu Bar Settings</a> and set 'Automatically hide and show the menu bar to 'Always'. 
   
This gives your desktop a much more focussed appearance by eliminating OS "chrome".

From now on, you can just <span class="key">⌘</span> <span class="key">⇥</span> to cycle through apps or <span class="key">⌘</span> <span class="key">␣</span> to search and open apps.

<div class="step" data-num="2">Install Rectangle</div>

<a class="link_preview" href="https://rectangleapp.com/" target="_blank">
    <img class="link_preview_icon" src="/static/rectangle_icon.png">
    <span class="link_preview_title">Rectangle</span>
    <span class="link_preview_description">Move and resize windows in macOS using keyboard shortcuts or snap areas.</span>
</a>

Rectangle is our tiling window manager. While holding <span class="key">⌘</span> <span class="key">⌥</span> and then tapping <span class="key">←</span> or <span class="key">→</span> you can move the active window to the left or right. You can set up quadrants, but I only ever find myself wanting 2 windows open at once- one on the left, one on the right.

<div class="step" data-num="3">Install Homerow</div>

<a class="link_preview" href="https://www.homerow.app/" target="_blank">
    <img class="link_preview_icon" src="/static/homerow_icon.png">
    <span class="link_preview_title">Homerow</span>
    <span class="link_preview_description">Keyboard shortcuts for every button in macOS</span>
</a>

Homerow enables you to never have to use your mouse again. By typing <span class="key">⌘</span> <span class="key">⇧</span> <span class="key">␣</span>, any interactive element on the window is now "clickable" by typing the corresponding 1-2 character combination.

<div class="step" data-num="4">Install Superwhisper</div>

<a class="link_preview" href="https://superwhisper.com/" target="_blank">
    <img class="link_preview_icon" src="/static/superwhisper_icon.png">
    <span class="link_preview_title">Superwhisper</span>
    <span class="link_preview_description">Write 3x faster without lifting a finger</span>
</a>

Lastly, I find myself really enjoying Slacking, Emailing, Messaging, ChatGPTing using Superwhisper. It's a great way to "type" when precision is not required. I just type <span class="key">⌥</span><span class="key">A</span> to start dictating in any focussed field and then <span class="key">⌥</span><span class="key">A</span> again to stop and paste. So almost any time my writing will be interpreted by another person, I use Superwhisper to get the idea across with just my voice.

### To Explore...

These tools have sped up how I use my computer. It has me wondering what else I don't know about that others use to get even closer to the speed of thought. I'd be very interested to try out an eye tracker or even a BCI to see if any of them are faster than Homerow.

[^1]: [Omarchy](https://omarchy.org/)
[^2]: [Framework Computers](https://frame.work/ca/en)
[^3]: [Omarchy on a Macbook with Asahi guide](https://github.com/basecamp/omarchy/discussions/155)

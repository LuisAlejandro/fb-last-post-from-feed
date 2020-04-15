<p align='center'>
  <h3 align="center">fb-last-post-from-feed</h3>
  <p align="center">GitHub Action for posting to a facebook page the latest entry from an atom feed</p>
</p>

---

Current version: 0.1.0

## 🎒 Prep Work
1. [Get a facebook permanent access token](https://stackoverflow.com/a/28418469/911071) using a facebook account that owns the page where you want to post messages.
2. [Find the ID](https://www.facebook.com/help/1503421039731588) of the page that you want to post messages in.
2. Find the atom feed URL that contains the posts that you wish to share.

## 🖥 Project Setup
1. Fork this repo.
2. Go to your fork's `Settings` > `Secrets` > `Add a new secret` for each environment secret (below).
3. Activate github workflows on `Actions` > `I understand my workflows, go ahead and run them`.
4. Star your own fork to trigger the initial build. The feed is checked hourly, if you haven't posted anything on your blog on the last hour, nothing will be posted on the initial build.

## 🤫 Environment Secrets

- **FACEBOOK_PAGE_ID**: The page ID where you want to post
- **FACEBOOK_ACCESS_TOKEN**: The permanent facebook access token
- **FEED_URL**: Atom feed URL

## How to get a Facebook permanent access token

Following the instructions laid out in Facebook's [extending page tokens documentation][2] I was able to get a page access token that does not expire.

I suggest using the [Graph API Explorer][3] for all of these steps except where otherwise stated.

### 0. Create Facebook App ###

**If you already have an app**, skip to step 1.

1. Go to [My Apps][4].
2. Click "+ Add a New App".
3. Setup a website app.

You don't need to change its permissions or anything. You just need an app that wont go away before you're done with your access token.

### 1. Get User Short-Lived Access Token ###

1. Go to the [Graph API Explorer][3].
2. Select the application you want to get the access token for (in the "Application" drop-down menu, not the "My Apps" menu).
3. Click "Get Token" > "Get User Access Token".
4. In the pop-up, under the "Extended Permissions" tab, check "manage_pages".
5. Click "Get Access Token".
6. Grant access from a Facebook account that has access to manage the target page. Note that if this user loses access the final, never-expiring access token will likely stop working.

The token that appears in the "Access Token" field is your short-lived access token.

### 2. Generate Long-Lived Access Token ###

Following [these instructions][5] from the Facebook docs, make a GET request to

> https://graph.facebook.com/v2.10/oauth/access_token?grant_type=fb_exchange_token&client_id=**{app_id}**&client_secret=**{app_secret}**&fb_exchange_token=**{short_lived_token}**

entering in your app's ID and secret and the short-lived token generated in the previous step.

You **cannot use the Graph API Explorer**. For some reason it gets stuck on this request. I think it's because the response isn't JSON, but a query string. Since it's a GET request, you can just go to the URL in your browser.

The response should look like this:

> {"access_token":"**ABC123**","token_type":"bearer","expires_in":5183791}

"ABC123" will be your long-lived access token. You can put it into the [Access Token Debugger][7] to verify. Under "Expires" it should have something like "2 months".

### 3. Get User ID ###

Using the long-lived access token, make a GET request to 

> https://graph.facebook.com/v2.10/me?access_token=**{long_lived_access_token}**

The `id` field is your account ID. You'll need it for the next step.

### 4. Get Permanent Page Access Token ###

Make a GET request to

> https://graph.facebook.com/v2.10/**{account_id}**/accounts?access_token=**{long_lived_access_token}**

The JSON response should have a `data` field under which is an array of items the user has access to. Find the item for the page you want the permanent access token from. The `access_token` field should have your permanent access token. Copy it and test it in the [Access Token Debugger][7]. Under "Expires" it should say "Never".

[2]:https://developers.facebook.com/docs/facebook-login/access-tokens#extendingpagetokens
[3]:https://developers.facebook.com/tools/explorer
[4]:https://developers.facebook.com/apps/
[5]:https://developers.facebook.com/docs/facebook-login/access-tokens#extending
[6]:https://luckymarmot.com/paw
[7]:https://developers.facebook.com/tools/debug/accesstoken
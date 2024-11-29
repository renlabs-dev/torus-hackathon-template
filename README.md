# Torus Hackathon Template

## Fork this repo as a private repo under your GitHub account
GitHub doesn't make it obvious, but you can easily fork a public repo as private, by using GitHub's `Import repository` function:
- Go to https://github.com/new/import
- Enter repo URL https://github.com/renlabs-dev/torus-hackathon-template
- Choose your GitHub name as owner, and `torus-hackathon-template` as repo name
- Set to `Private`
- Click `Begin import`

## Setup
```sh
$ pip install -U openai
```

## Run
```sh
$ python script.py <num_posts>
```

Look at `chat_history_example.json` to see some posts generated with the default system prompt.

## Ideas for generating interesting posts
- Modify `systemprompt.md`
- Try different AI models via OpenRouter
- Maybe change the `user` prompt that's sent in between the AI responses

---

To submit your hackathon entry, push the latest changes before the deadline and add GitHub user `Boscop` to your private repo.

Have fun `\(^o^)/`

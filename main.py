import os
import requests
import scratchattach as scratch3
import keep_alive

API_KEY = os.environ['API_KEY']

conn = scratch3.TwCloudConnection(
  project_id="850366286")  #replace with your project id
client = scratch3.TwCloudRequests(conn)

USER_TOKEN = "<|prompter|>"
ASSISTANT_TOKEN = "<|assistant|>"
ENDPOINT_TOKEN = "<|endoftext|>"

API_URL = "https://api-inference.huggingface.co/models/OpenAssistant/oasst-sft-4-pythia-12b-epoch-3.5"
headers = {"Authorization": "Bearer " + API_KEY}


def query(payload):
  response = requests.post(API_URL, headers=headers, json=payload)
  return response.json()


def prompt(p):
  output = [{"generated_text": ""}]
  for i in range(15):
    last_value = output
    output = query({
      "inputs": p + output[0]['generated_text'],
    })
    if last_value == output:
      break

  output = output[0]['generated_text']
  #output = output.split(ASSISTANT_TOKEN)[-1].split(ENDPOINT_TOKEN)[0]
  return output


def fixed_input(value):
  fixed_input = value
  fixed_input = fixed_input.replace("|prompter|", USER_TOKEN)
  fixed_input = fixed_input.replace("|assistant|", ASSISTANT_TOKEN)
  fixed_input = fixed_input.replace("|endoftext|", ENDPOINT_TOKEN)
  return fixed_input


@client.request
def Premium(argument1):
  return str(True)


@client.request
def ASK_AI(argumant1):
  requester = client.get_requester()
  fixed_prompt = fixed_input(argumant1)
  print(
    f'{requester} asked \"{fixed_prompt.split(USER_TOKEN)[-1].split(ENDPOINT_TOKEN)[0]}\" to NexusGPT'
  )
  try:
    answer = prompt(fixed_prompt)
    answer = answer.split(ASSISTANT_TOKEN)[-1].split(ENDPOINT_TOKEN)[0]
  except:
    answer = "Sorry, I don't understand :("
  #if "Open Assistant" in answer:
  #answer = answer.remplace("Open Assistant", "NexusGPT")
  print(f'NexusGPT returned \"{answer}\" to NexusGPTto {requester}')
  return answer


@client.event
def on_ready():
  print("Request handler is running")


keep_alive.keep_alive

client.run()

#Here is some text

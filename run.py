import requests
import json
import openai

OPENAI_API_KEY = 'Add your api key here'
client = openai.OpenAI(api_key=OPENAI_API_KEY)
openai.api_key = OPENAI_API_KEY
def generate_prompt():
    gpt_assistant_prompt = "You are a instagram account holder who wants to get maximum outreach in the audience. You want to post their relaistic pictures of a happy dalmatian dog who has been doing an activity that a human does. You will be posting one image daily so the activitiy you choose today should not be same as anything generated before. You do not want any caption on image."
    gpt_user_prompt = "Please generate a prompt for realistic photo that I can use to generate these pictures via software. Write just one activity. Please be creative here with the activities."
    gpt_prompt = gpt_assistant_prompt, gpt_user_prompt
    message = [{"role": "assistant", "content": gpt_assistant_prompt}, {"role": "user", "content": gpt_user_prompt}]
    temperature = 0.2
    max_tokens = 256
    frequency_penalty = 0.0
    response = client.chat.completions.create(
        model="gpt-4",
        messages = message,
        # temperature=temperature,
        # max_tokens=max_tokens,
        # frequency_penalty=frequency_penalty

    )
    return response.choices[0].message.content




def generate_hashtags(prompt):
    gpt_assistant_prompt = "You are a instagram account holder who wants to get maximum outreach in the audience. You want to post their relaistic pictures of dalmatian dog who has been doing an activity that a human does. Please optimise SEOs to reach the maximum audience"
    # gpt_user_prompt = "generate instagram hashtags with a caption about an image that depicts: A supercute realistic dalmatian celebrating St. Patrick Day and is happy about it"
    gpt_user_prompt = "generate instagram hashtags with a caption about an image that depicts : {}".format(prompt)
    gpt_prompt = gpt_assistant_prompt, gpt_user_prompt
    message = [{"role": "assistant", "content": gpt_assistant_prompt}, {"role": "user", "content": gpt_user_prompt}]
    temperature = 0.2
    max_tokens = 256
    frequency_penalty = 0.0
    response = client.chat.completions.create(
        model="gpt-4",
        messages = message,
        # temperature=temperature,
        # max_tokens=max_tokens,
        # frequency_penalty=frequency_penalty

    )
    return response.choices[0].message.content


def create_image(PROMPT):
   response = client.images.generate(
       model="dall-e-3",
       quality="standard",
      prompt=PROMPT,
      n=1,
      size="1024x1024",
      )
   return response.data[0].url




def postInstagramQuote():
#Post the Image
    ig_user_id = "Add your insta ig id"
    user_access_token = "add your access token"
    # prompt = "A supercute realistic dalmatian celebrating St. Patrick Day and is happy about it"
    prompt = generate_prompt()
    print("prompt:", prompt)
    image_location_1 = create_image(prompt)
    post_url = 'https://graph.facebook.com/v19.0/{}/media'.format(ig_user_id)
    payload = {
    'image_url': image_location_1,
    'caption': generate_hashtags(prompt),
    'access_token': user_access_token
    }
    print(payload)
    r = requests.post(post_url, data=payload)
    print(r.text)
    result = json.loads(r.text)
    if 'id' in result:
        creation_id = result['id']
        second_url = 'https://graph.facebook.com/v19.0/{}/media_publish'.format(ig_user_id)
        second_payload = {
        'creation_id': creation_id,
        'access_token': user_access_token
        }
        r = requests.post(second_url, data=second_payload)
        print('--------Just posted a post to instagram--------')
        print(r.text)
    else:
        print('HOUSTON we have a problem in posting post!')

    # Post a story of the same
    post_url = 'https://graph.facebook.com/v19.0/{}/media'.format(ig_user_id)
    payload = {
        'image_url': image_location_1,
        'media_type': 'STORIES',
        'caption': generate_hashtags(prompt),
        'access_token': user_access_token
    }
    print(payload)
    r = requests.post(post_url, data=payload)
    print(r.text)
    result = json.loads(r.text)
    if 'id' in result:
        creation_id = result['id']
        second_url = 'https://graph.facebook.com/v19.0/{}/media_publish'.format(ig_user_id)
        second_payload = {
            'creation_id': creation_id,
            'access_token': user_access_token
        }
        r = requests.post(second_url, data=second_payload)
        print('--------Just posted story to instagram--------')
        print(r.text)
    else:
        print('HOUSTON we have a problem in posting a story!')

postInstagramQuote()
import pyeuropeana as pe
import pyeuropeana.apis as apis
import pyeuropeana.utils as utils
import os
import pandas as pd

os.environ['EUROPEANA_API_KEY'] = 'armedinguil'
pd.set_option('display.max_colwidth', 15)


#Search API

# # use this function to search our collections
# result = apis.search(
#     query = '*',
#     qf = '(skos_concept:"http://data.europeana.eu/concept/base/48" AND TYPE:IMAGE)',
#     reusability = 'open AND permission',
#     media = True,
#     thumbnail = True,
#     landingpage = True,
#     colourpalette = '#0000FF',
#     theme = 'photography',
#     sort = 'europeana_id',
#     profile = 'rich',
#     rows = 1000,
#     ) # this gives you full response metadata along with cultural heritage object metadata

#     # use this utility function to transform a subset of the cultural heritage object metadata
#     # into a readable Pandas DataFrame
# dataframe = utils.search2df(result)

# #Record API

# import pyeuropeana.apis as apis

# # gets the metadata from an object using its europeana id
# data = apis.record('/79/resource_document_museumboerhaave_V35167')

#Entity API

resp = apis.entity.suggest(
   text = 'leonardo',
   TYPE = 'agent',
)

print(resp.keys())

print(resp['total'])

print(len(resp['items']))

df = pd.json_normalize(resp['items'])
cols = df.columns.tolist()
cols = cols[-2:]+cols[:-2]
df = df[cols]

rm_cols = [col for col in df.columns if 'isShownBy' in col]
df = df.drop(columns=rm_cols)
print(df.head())

resp = apis.entity.retrieve(
   TYPE = 'agent',
   IDENTIFIER = 146741,
)

# # print(resp.keys())

def get_name_df(resp):
  lang_name_df = None
  if 'prefLabel' in resp.keys():
    lang_name_df = pd.DataFrame([{'language':lang,'name':name} for lang,name in resp['prefLabel'].items()])
  return lang_name_df

lang_name_df = get_name_df(resp)
print(lang_name_df.head())


# def get_biography_df(resp):
#   bio_df = None
#   if 'biographicalInformation' in resp.keys():
#     bio_df = pd.DataFrame(resp['biographicalInformation'])
#   return bio_df

# bio_df = get_biography_df(resp)
# print(bio_df)

# #bio_df['@name'].loc[bio_df['@language'] == 'en'].values[0]

# def get_bio_uri(uri):
#   id = int(uri.split('/')[-1])
#   resp = apis.entity.retrieve(
#     TYPE = 'agent',
#     IDENTIFIER = id,
#   )

#   bio_df = get_biography_df(resp)
#   bio = bio_df.loc[bio_df['@language'] == 'en'].values[0]
#   return bio

# df['bio'] = df['id'].apply(get_bio_uri)
# print(df.head())


def get_place_resp(resp, event):

  if event == 'birth':
    if 'placeOfBirth' not in resp.keys():
      return
    place = resp['placeOfBirth']

  elif event == 'death':
    if 'placeOfDeath' not in resp.keys():
      return
    place = resp['placeOfDeath']

  if not place:
    return

  #place = list(place[0].values())[0]

  if place.startswith('http'):
     place = place.split('/')[-1].replace('_',' ')
  return place



resp = apis.entity.retrieve(
   TYPE = 'agent',
   IDENTIFIER = 146741,
)
print(get_place_resp(resp, 'birth'))

def get_place(uri,event):
  id = int(uri.split('/')[-1])
  resp = apis.entity.retrieve(
    TYPE = 'agent',
    IDENTIFIER = id,
  )
  return get_place_resp(resp,event)


df['placeOfBirth'] = df['id'].apply(lambda x: get_place(x,'birth'))
df['placeOfDeath'] = df['id'].apply(lambda x: get_place(x,'death'))
print(df.head())

resp = apis.entity.suggest(
   text = 'Marguerite Gerard',
   TYPE = 'agent',
)

df = pd.json_normalize(resp['items'])
df = df.drop(columns=[col for col in df.columns if 'isShownBy' in col])
#df['bio'] = df['id'].apply(get_bio_uri)
df['placeOfBirth'] = df['id'].apply(lambda x: get_place(x,'birth'))
df['placeOfDeath'] = df['id'].apply(lambda x: get_place(x,'death'))
print(df.head())

resp = apis.entity.resolve('http://dbpedia.org/resource/Leonardo_da_Vinci')
resp.keys()

#IIIF API

# The IIIF API is mostly used to access newspapers collections at Europeana

# returns a minimal set of metadata for an object
# data = apis.iiif.manifest('/9200356/BibliographicResource_3000118390149')

# # returns text and annotations for a given page of an object
# data = apis.iiif.annopage(
#   RECORD_ID = '/9200356/BibliographicResource_3000118390149',
#   PAGE_ID = 1
# )

# # returns the transciption of a single page of a newspaper
# data = apis.iiif.fulltext(
#   RECORD_ID = '/9200396/BibliographicResource_3000118435063',
#   FULLTEXT_ID = '8ebb67ccf9f8a1dcc2ea119c60954111'
# )

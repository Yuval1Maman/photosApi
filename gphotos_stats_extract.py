items = []
nextpagetoken = None
# The default number of media items to return at a time is 25. The maximum pageSize is 100.
while nextpagetoken != '':
    print(f"Number of items processed:{len(items)}", end='\r')
    results = google_photos.mediaItems().list(pageSize=100, pageToken=nextpagetoken).execute()
    items += results.get('mediaItems', [])
    nextpagetoken = results.get('nextPageToken', '')
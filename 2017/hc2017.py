import fileinput
import sys

class Cache:
	def __init__(self, id_, tot_size):
		self._id = id_
		self._tot_size = tot_size
		self._free_size = tot_size	
		self._endpoint_list = []
		self._video_list = []
	def __str__(self):
		return 'Cache {} with total size {} and connected to {}'.format(self._id, self._tot_size, self._endpoint_list)
	def addEP(self, ep):
		self._endpoint_list.append(ep)

class EndPoint:
	#cache_dict = {id_cache : latenza}
	def __init__(self, id_, cache_dict, lat_dc):
		self._id = id_
		self._cache_dict = cache_dict
		self._L_DC = lat_dc
		self._rqs = []
	def __str__(self):
		return 'EndPoint {} with cache dictionary {} and latency form DC {} and requests {}'.format(self._id, self._cache_dict, self._L_DC, self._rqs)
	def addRqs(self, rqs):
		flag = 0
		for r in self._rqs:
			if r._id_video == rqs._id_video:
				r._freq += rqs._freq
				flag = 1
		if flag == 0:
			self._rqs.append(rqs)

class Request:
	def __init__(self, id_video, endpoint_id, freq):
		self._id_video = id_video
		self._endpoint_id = endpoint_id
		self._freq = freq
	def __str__(self):
		return 'Request video {} from {} with {}'.format(self._id_video, self._endpoint_id, self._freq)
	

endPoint_list = []
cache_list = []
request_list = {}
video_dict = {}

def main():
	input = fileinput.input()
	V, E, R, C, X = map(int, input.readline().split(' '))
	# INIT CACHE
	for i in xrange(C):
		cache_list.append(Cache(i, X))
	video_dict = dict(zip(range(V), map(int, input.readline().split(' '))))
	# INIT ENDPOINT
	for endpoint_id in xrange(E):
		#L_DC = latenza datacenter
		L_DC, n_caches = map(int, input.readline().split(' '))
		cache_dict = {}
		for j in xrange(n_caches):
			ID_CACHE, L = map(int, input.readline().split(' '))
			cache_dict[ID_CACHE] = L
			cache_list[ID_CACHE].addEP(endpoint_id)

		endpoint = EndPoint(endpoint_id, cache_dict, L_DC)
		endPoint_list.append(endpoint)
	# INIT REQUEST
	for i in xrange(R):
		id_video, endpoint_id, freq = map(int, input.readline().split(' '))
		rqs = Request(id_video, endpoint_id, freq)
		'''
		#flag = 0
		#for r in request_list:
		try:
			freqR = request_list[(rqs._id_video, rqs._endpoint_id)]
			if (freqR != freq):
				request_list[(rqs._id_video, rqs._endpoint_id)] = request_list[(rqs._id_video, rqs._endpoint_id)] + freq
			#if r._id_video == rqs._id_video and r._endpoint_id == rqs._endpoint_id and not (r._freq == rqs._freq):
				#r._freq += rqs._freq
				#flag = 1
		except:
			request_list[(rqs._id_video, rqs._endpoint_id)] = freq
		'''
		endPoint_list[endpoint_id].addRqs(rqs)

		
	for cache in cache_list:
		all_rqs = []
		for id_ep in cache._endpoint_list:
			for r in endPoint_list[id_ep]._rqs:
				all_rqs.append(r)
		while cache._free_size > 0 and len(all_rqs) > 0:
			r = max(all_rqs, key=lambda x: x._freq)
			if (cache._free_size - video_dict[r._id_video]) > 0:
				cache._video_list.append(r._id_video)
				cache._free_size -= video_dict[r._id_video]
				all_rqs.remove(r)
				endPoint_list[r._endpoint_id]._rqs.remove(r)
				all_rqs = [tr for tr in all_rqs if tr._id_video != r._id_video]		
			else:
				break
		print '{} {}'.format(cache._id, ' '.join(map(str, cache._video_list)))
	#print '{}'.format(len([x for x in cache_list if len(x._video_list) != 0]))
        #for cache in cache_list:
	#	print '{} {}'.format(cache._id, ' '.join(map(str, cache._video_list)))



if __name__ == '__main__':
	main()

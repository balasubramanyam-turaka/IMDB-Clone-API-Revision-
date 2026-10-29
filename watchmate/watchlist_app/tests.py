from django.contrib.auth.models import User
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from watchlist_app.models import StreamPlatform, WatchList, Review
class StreamPlatformTestCase(APITestCase):
  def setUp(self):
    self.user = User.objects.create_user(username='example1', password='example@123')
    self.token = Token.objects.get(user__username='example1')
    self.client.credentials(HTTP_AUTHORIZATION='Token '+ self.token.key)
    
    self.stream = StreamPlatform.objects.create(name='Netflix', about='#1 Streaming Platform in world', website='https://netflix.com')
    
  def test_streamplatform_create(self):
    data = {
      'name':'Netflix',
      'about':'#1 Streaming Platform in world',
      'website':'https://netflix.com'
    }
    
    response = self.client.post(reverse('streamplatform-list'), data)
    self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
  def test_streamplatform_list(self):
    response = self.client.get(reverse('streamplatform-list'))
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    
  def test_streamplatform_ind(self):
    response = self.client.get(reverse('streamplatform-detail', args=(self.stream.id,)))
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    
  def test_streamplatform_del(self):
    response = self.client.delete(reverse('streamplatform-detail', args=(self.stream.id,)))
    self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
class WatchListTestCase(APITestCase):
  
  def setUp(self):
    self.user = User.objects.create_user(username='example1', password='example@123')
    self.token = Token.objects.get(user__username='example1')
    self.client.credentials(HTTP_AUTHORIZATION='Token '+ self.token.key)
    
    self.stream = StreamPlatform.objects.create(name='Netflix', about='#1 Streaming Platform in world', website='https://netflix.com')
    
    self.watchlist = WatchList.objects.create(title='Example Movie', description='This movie is Raw and Rustic Movie', platform=self.stream, active=True)
    
  def test_watchlist_create(self):
    data = {
      'title':'Example Movie',
      'description':'This movie is Raw and Rustic Movie',
      'paltform':self.stream,
      'active':True
    }
    
    response = self.client.post(reverse('watchlist-list'), data)
    self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
  def test_watchlist_list(self):
    response = self.client.get(reverse('watchlist-list'))
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    
  def test_watchlist_ind(self):
    response = self.client.get(reverse('watchlist-detail', args=(self.watchlist.id,)))
    self.assertEqual(response.status_code, status.HTTP_200_OK) 
    self.assertEqual(WatchList.objects.get().title, 'Example Movie')
    self.assertEqual(WatchList.objects.count(), 1)
    
    
    
class ReviewTestCase(APITestCase):
  def setUp(self):
    self.user = User.objects.create_user(username='example1', password='example@123')
    self.token = Token.objects.get(user__username='example1')
    self.client.credentials(HTTP_AUTHORIZATION='Token '+ self.token.key)
    
    self.stream = StreamPlatform.objects.create(name='Netflix', about='#1 Streaming Platform in world', website='https://netflix.com')
    
    self.watchlist = WatchList.objects.create(title='Example Movie', description='This movie is Raw and Rustic Movie', platform=self.stream, active=True)
    
    self.watchlist2 = WatchList.objects.create(title='Example Movie 2', description='This movie is Raw and Rustic Movie', platform=self.stream, active=True)
    self.review = Review.objects.create(review_user=self.user, rating = 5, description='Suberb movie!', watchlist=self.watchlist2, active=True)
  
  def test_review_create(self):
    data ={
      'review_user':self.user,
      'rating':5,
      'description':'Superb movie!',
      'watchlist':self.watchlist,
      'active':True
    }
    
    response = self.client.post(reverse('review-create', args=(self.watchlist.id,)), data)
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    self.assertEqual(Review.objects.count(), 2)
    
    
    response = self.client.post(reverse('review-create', args=(self.watchlist2.id,)), data)
    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
  def test_review_create_unauth(self):
    data ={
          'review_user':self.user,
          'rating':5,
          'description':'Superb movie!',
          'watchlist':self.watchlist,
          'active':True
        }
    self.client.force_authenticate(user=None)
    response = self.client.post(reverse('review-create', args=(self.watchlist.id,)), data)
    self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
  
  def test_review_update(self):
    data ={
              'review_user':self.user,
              'rating':4,
              'description':'Superb movie! - Updated',
              'watchlist':self.watchlist,
              'active':False
            }
    response = self.client.put(reverse('review-detail', args=(self.review.id,)), data)
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    
  
  
  def test_review_list(self):
    response = self.client.get(reverse('review-list', args=(self.watchlist.id, )))
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    
  def test_review_ind(self):
    response = self.client.get(reverse('review-detail', args=(self.review.id, )))
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    
  def test_review_del(self):
      response = self.client.delete(reverse('review-detail', args=(self.review.id, )))
      self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
      
      
  def test_review_user(self):
    response = self.client.get('/watchlist/review/?username' + self.user.username)
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    
  
    
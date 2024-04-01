import unittest
from unittest.mock import MagicMock, patch
from your_module import fetch_reddit_data, store_data_to_csv, generate_newsletter, send_to_buttondown

class TestRedditNewsletter(unittest.TestCase):
    
    @patch('your_module.praw.Reddit')
    def test_fetch_reddit_data(self, mock_reddit):
        # Mock the PRAW Reddit instance and its methods
        mock_post = MagicMock()
        mock_post.title = 'Test Post'
        mock_post.url = 'https://test.com'
        mock_post.score = 100
        mock_post.num_comments = 50
        
        mock_comment = MagicMock()
        mock_comment.body = 'Test Comment'
        mock_comment.score = 10
        
        mock_reddit.return_value.subreddit.return_value.hot.return_value = [mock_post] * 10
        mock_reddit.return_value.subreddit.return_value.controversial.return_value = [mock_post] * 10
        mock_reddit.return_value.subreddit.return_value.top.return_value = [mock_post] * 10
        mock_post.comments.list.return_value = [mock_comment] * 20
        
        # Call the function to fetch data
        data = fetch_reddit_data()
        
        # Assert the expected number of posts and comments
        self.assertEqual(len(data['hottest_posts']), 10)
        self.assertEqual(len(data['controversial_posts']), 10)
        self.assertEqual(len(data['top_posts']), 10)
        
        # Assert the structure and content of the retrieved data
        for post in data['hottest_posts']:
            self.assertEqual(post['title'], 'Test Post')
            self.assertEqual(post['url'], 'https://test.com')
            self.assertEqual(post['score'], 100)
            self.assertEqual(post['num_comments'], 50)
            self.assertEqual(len(post['comments']), 20)
            for comment in post['comments']:
                self.assertEqual(comment['body'], 'Test Comment')
                self.assertEqual(comment['score'], 10)
        
        # Similar assertions for controversial_posts and top_posts
    
    @patch('your_module.csv.writer')
    def test_store_data_to_csv(self, mock_csv_writer):
        # Mock the CSV writer
        mock_file = MagicMock()
        
        # Define test data
        test_data = [
            {'title': 'Test Post 1', 'url': 'https://test1.com', 'score': 100, 'num_comments': 50, 
             'comments': [{'body': 'Test Comment 1', 'score': 10}, {'body': 'Test Comment 2', 'score': 5}]},
            {'title': 'Test Post 2', 'url': 'https://test2.com', 'score': 200, 'num_comments': 80, 
             'comments': [{'body': 'Test Comment 3', 'score': 15}, {'body': 'Test Comment 4', 'score': 8}]}
        ]
        
        # Call the function to store data
        store_data_to_csv(mock_file, test_data)
        
        # Assert that the CSV writer was called with the expected data
        mock_csv_writer.return_value.writerow.assert_any_call(['title', 'url', 'score', 'num_comments', 'comment_body', 'comment_score'])
        mock_csv_writer.return_value.writerow.assert_any_call(['Test Post 1', 'https://test1.com', 100, 50, 'Test Comment 1', 10])
        mock_csv_writer.return_value.writerow.assert_any_call(['Test Post 1', 'https://test1.com', 100, 50, 'Test Comment 2', 5])
        mock_csv_writer.return_value.writerow.assert_any_call(['Test Post 2', 'https://test2.com', 200, 80, 'Test Comment 3', 15])
        mock_csv_writer.return_value.writerow.assert_any_call(['Test Post 2', 'https://test2.com', 200, 80, 'Test Comment 4', 8])
    
    @patch('your_module.dagster_openai.openai_completion')
    def test_generate_newsletter(self, mock_openai_completion):
        # Mock the OpenAI completion response
        mock_openai_completion.return_value = 'Generated newsletter content'
        
        # Define test data
        test_data = [
            {'title': 'Test Post 1', 'url': 'https://test1.com', 'score': 100, 'num_comments': 50, 
             'comments': [{'body': 'Test Comment 1', 'score': 10}, {'body': 'Test Comment 2', 'score': 5}]},
            {'title': 'Test Post 2', 'url': 'https://test2.com', 'score': 200, 'num_comments': 80, 
             'comments': [{'body': 'Test Comment 3', 'score': 15}, {'body': 'Test Comment 4', 'score': 8}]}
        ]
        
        # Call the function to generate the newsletter
        newsletter = generate_newsletter(test_data)
        
        # Assert the generated newsletter content
        self.assertEqual(newsletter, 'Generated newsletter content')
        
        # Assert that the OpenAI completion function was called with the expected prompt
        expected_prompt = "Generate an engaging newsletter based on the following Reddit posts and comments:\n\n"
        expected_prompt += "Post 1: Test Post 1 (https://test1.com)\nScore: 100\nNumber of Comments: 50\n"
        expected_prompt += "Comment 1: Test Comment 1 (Score: 10)\nComment 2: Test Comment 2 (Score: 5)\n\n"
        expected_prompt += "Post 2: Test Post 2 (https://test3.com)\nScore: 200\nNumber of Comments: 80\n"
        expected_prompt += "Comment 1: Test Comment 3 (Score: 15)\nComment 2: Test Comment 4 (Score: 8)\n\n"
        mock_openai_completion.assert_called_once_with(prompt=expected_prompt)
    
    @patch('your_module.requests.post')
    def test_send_to_buttondown(self, mock_post):
        # Mock the response from the Buttondown API
        mock_response = MagicMock()
        mock_response.status_code = 201
        mock_response.json.return_value = {'id': 'draft_123', 'subject': 'Test Newsletter', 'body': 'Test newsletter content'}
        mock_post.return_value = mock_response
        
        # Call the function to send the newsletter to Buttondown
        response = send_to_buttondown('Test Newsletter', 'Test newsletter content')
        
        # Assert the response status code and content
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()['id'], 'draft_123')
        self.assertEqual(response.json()['subject'], 'Test Newsletter')
        self.assertEqual(response.json()['body'], 'Test newsletter content')
        
        # Assert that the requests.post function was called with the expected data
        expected_url = 'https://api.buttondown.email/v1/drafts'
        expected_data = {
            'subject': 'Test Newsletter',
            'body': 'Test newsletter content'
        }
        mock_post.assert_called_once_with(expected_url, json=expected_data, headers={'Authorization': 'Token YOUR_API_TOKEN'})
        
    @patch('your_module.dagster_openai.openai_completion')
    def test_edit_newsletter(self, mock_openai_completion):
        # Mock the OpenAI completion response
        mock_openai_completion.return_value = 'Edited newsletter content'
        
        # Define test data
        test_newsletter = 'Generated newsletter content'
        
        # Call the function to edit the newsletter
        edited_newsletter = edit_newsletter(test_newsletter)
        
        # Assert the edited newsletter content
        self.assertEqual(edited_newsletter, 'Edited newsletter content')
        
        # Assert that the OpenAI completion function was called with the expected prompt
        expected_prompt = "Please edit the following newsletter for errors and ensure it adheres to markdown format with newlines:\n\n"
        expected_prompt += test_newsletter
        mock_openai_completion.assert_called_once_with(prompt=expected_prompt)
    
    def test_validate_newsletter(self):
        # Define test data
        valid_newsletter = {
            'subject': 'Test Newsletter',
            'body': 'Test newsletter content'
        }
        invalid_newsletter = {
            'subject': 'Test Newsletter',
            'invalid_field': 'Invalid content'
        }
        
        # Call the function to validate the newsletter
        self.assertTrue(validate_newsletter(valid_newsletter))
        self.assertFalse(validate_newsletter(invalid_newsletter))
    @patch('your_module.requests.post')
    def second_test_send_to_buttondown(self, mock_post):
        # Mock the response from the Buttondown API
        mock_response = MagicMock()
        mock_response.status_code = 201
        mock_response.json.return_value = {'id': 'draft_123', 'subject': 'Test Newsletter', 'body': 'Test newsletter content'}
        mock_post.return_value = mock_response
        
        # Define test data
        test_newsletter = {
            'subject': 'Test Newsletter',
            'body': 'Test newsletter content'
        }
        
        # Call the function to send the newsletter to Buttondown
        response = send_to_buttondown(test_newsletter)
        
        # Assert the response status code and content
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()['id'], 'draft_123')
        self.assertEqual(response.json()['subject'], 'Test Newsletter')
        self.assertEqual(response.json()['body'], 'Test newsletter content')
        
        # Assert that the requests.post function was called with the expected data
        expected_url = 'https://api.buttondown.email/v1/drafts'
        mock_post.assert_called_once_with(expected_url, json=test_newsletter, headers={'Authorization': 'Token YOUR_API_TOKEN'})
    @patch('your_module.fetch_reddit_data')
    @patch('your_module.store_data_to_csv')
    @patch('your_module.generate_newsletter')
    @patch('your_module.edit_newsletter')
    @patch('your_module.validate_newsletter')
    @patch('your_module.send_to_buttondown')
    def test_pipeline(self, mock_send_to_buttondown, mock_validate_newsletter, mock_edit_newsletter, 
                        mock_generate_newsletter, mock_store_data_to_csv, mock_fetch_reddit_data):
            # Mock the return values of the pipeline steps
            mock_fetch_reddit_data.return_value = [
                {'title': 'Test Post 1', 'url': 'https://test1.com', 'score': 100, 'num_comments': 50, 
                'comments': [{'body': 'Test Comment 1', 'score': 10}, {'body': 'Test Comment 2', 'score': 5}]},
                {'title': 'Test Post 2', 'url': 'https://test2.com', 'score': 200, 'num_comments': 80, 
                'comments': [{'body': 'Test Comment 3', 'score': 15}, {'body': 'Test Comment 4', 'score': 8}]}
            ]
            mock_generate_newsletter.return_value = 'Generated newsletter content'
            mock_edit_newsletter.return_value = 'Edited newsletter content'
            mock_validate_newsletter.return_value = True
            mock_send_to_buttondown.return_value = MagicMock(status_code=201)
        
            # Call the pipeline function
            pipeline_result = your_module.pipeline()
        
            # Assert that each step of the pipeline was called with the expected arguments
            mock_fetch_reddit_data.assert_called_once()
            mock_store_data_to_csv.assert_called_once_with(unittest.mock.ANY, mock_fetch_reddit_data.return_value)
            mock_generate_newsletter.assert_called_once_with(mock_fetch_reddit_data.return_value)
            mock_edit_newsletter.assert_called_once_with('Generated newsletter content')
            mock_validate_newsletter.assert_called_once_with({'subject': unittest.mock.ANY, 'body': 'Edited newsletter content'})
            mock_send_to_buttondown.assert_called_once_with({'subject': unittest.mock.ANY, 'body': 'Edited newsletter content'})
        
            # Assert the pipeline result
            self.assertEqual(pipeline_result, {'status_code': 201})

if __name__ == '__main__':
    unittest.main()
            
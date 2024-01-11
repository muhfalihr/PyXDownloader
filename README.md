[![Instagram: ____mfr.py](https://img.shields.io/badge/Instagram-Follow%20Me-blue?style=social&logo=instagram)](https://www.instagram.com/_____mfr.py/)

# PyXDownloader

![ProjectImage](https://github.com/muhfalihr/mystorage/blob/master/20240109_202619.jpg)

**Tool Description:**
PyXDownloader is an advanced tool developed using the Python programming language to assist users in downloading posts from Twitter. With a simple and user-friendly interface, PyXDownloader allows users to quickly and efficiently retrieve content such as tweets, images, and videos from specific Twitter accounts.

Key features of PyXDownloader include:

1. **User-Centric Downloads:** Focuses on user-friendly content retrieval from specific Twitter accounts.
2. **Efficient Python Usage:** Built with the Python programming language, ensuring fast and efficient performance.
3. **Intuitive Graphic Interface:** A user-friendly interface design makes it easy for users to configure and execute downloads seamlessly.
4. **Content Filtering Options:** Enables users to customize downloads based on date, content type, or specific keywords.
5. **Download History Management:** Stores a history of downloads, allowing users to easily access and manage previously downloaded files.
6. **Regular Update Support:** Ensures the tool stays up-to-date with the latest changes or updates on the Twitter platform.

PyXDownloader is the ideal solution for those seeking a reliable and efficient tool to gather and manage content from Twitter accounts within the trusted Python programming environment. Explore the world of Twitter more easily and effectively with PyXDownloader.

## Requirements

- **Python**

  Already installed Python with version 3.10.12. See the [Installation and Setting up Python](https://github.com/muhfalihr/PyXDownloader/?tab=readme-ov-file#installation-of-python-31012).

- **Have an active Twitter account**

  Used to run programs because cookies are required from that account. If you don't have a Twitter account, you have to [log in](https://twitter.com/login) first.

## Clone the repository to your directory

```sh
# Change Directory
cd /home/ubuntu/Desktop

# Install gh
sudo apt install gh

# Auth gh
gh auth login

# Clonig Repository
gh repo clone muhfalihr/PyXDownloader
```

## Installation of Python 3.10.12

- Install Python version 3.

  ```sh
  apt install python3
  ```

- Instal Virtual environment for Python version 3.

  ```sh
  apt install python3-venv
  ```

- Create a Python virtual environment using the venv module.

  ```sh
  python3 -m venv .venv/my-venv
  ```

- Install the python package according to the requirements.txt file.
  ```sh
  .venv/my-venv/bin/pip install -r requirements.txt
  ```

## How to use ?

1. Enter your cookies into the **cookie** variables available in the **_pxd_** file.

   ```
   cookie = 'your-cookie'
   ```

2. You need to give execute permission to the Python file. Use the following command in terminal or command prompt:

   ```sh
   chmod +x pxd
   ```

3. Functions used in running the program. As follows :

   - **_Allmedias_**

     Downloads all media from a specific user's posts.

     ```sh
     ./pxd -sn <screen-name> -p /path/to/save
     ```

   - **_Images_**

     Downloads all images from the specified user's posts.

     ```sh
     ./pxd -f images -sn <screen-name> -p /path/to/save
     ```

   - **_LinkDownloader_**

     Downloads the specified media via the link provided.

     ```sh
     ./pxd -f linkdownloader -link http://example.org/media/12345678/abcdefg.jpg -p /path/to/save
     ```

### Description of the arguments used.

1. **_--function/-f_**

   Used to determine the name of the function that will execute the arguments entered.

2. **_--link/-link_**

   Used to determine the link from the user's post to be downloaded.

3. **_--path/-p_**

   Used to specify the path of the folder to save the download results.

4. **_--screenname/-sn_**

   Used to determine the screen name of the user whose media posts we will download.

5. **_--count/-count_**

   Used to determine the amount of media from user posts that will be downloaded. Even so, it won't affect anything because the response in the API is inconsistent.

6. **_--cursor/-cursor_**

   Used to retrieve the next API response.

## License

The PyXDownloader project is licensed by [MIT License](https://github.com/muhfalihr/PyXDownloader/blob/master/LICENSE).

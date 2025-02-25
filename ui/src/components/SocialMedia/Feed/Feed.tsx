import { useState, useEffect } from "react";
import NewPost from "./NewPost";
import NeumorphButton from "@/components/commons/neumorph-button";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faHeart } from "@fortawesome/free-regular-svg-icons/faHeart";
import { faComment, faShare } from "@fortawesome/free-solid-svg-icons";

interface IPost {
  id: number;
  userId: number;
  title: string;
  body: string;
}

interface IUser {
  id: number;
  name: string;
  username: string;
}

export default function Feed() {
  const [posts, setPosts] = useState<IPost[]>([]);
  const [users, setUsers] = useState<IUser[]>([]);

  const fetchUsers = () => {
    fetch("https://jsonplaceholder.typicode.com/users")
      .then((response) => response.json())
      .then((data) => {
        setUsers(data);
      });
  }

  const fetchPosts = () => {
    fetch("https://jsonplaceholder.typicode.com/posts")
      .then((response) => response.json())
      .then((data) => {
        const limitedData = data.slice(0, 10);
        setPosts(limitedData);
      });
  }

  useEffect(() => {
    fetchUsers();
    fetchPosts();
  }, []);

  return (
    <div className='flex flex-col items-center justify-start h-screen'>
      <div className="border-b border-gray-200 w-full"></div>
      <div className="w-full p-4">
        <NewPost />
      </div>
      <div className="border-b border-gray-200 w-full"></div>
      <div>
        {posts.map((post) => {
          const user = users.find((user) => user.id === post.userId);
          return (
            <>
              <div key={post.id} className='p-4 m-4'>
                <div>
                  <span className='text-sm font-bold'>{user?.name} </span>
                  <span className="text-sm text-gray-500"> @{user?.username}</span>
                </div>
                <p className='mb-2'>{post.body}</p>
                <div className='flex justify-start'>
                  <button className="text-xl mr-8">
                    <FontAwesomeIcon icon={faHeart} className='text-gray-500' />
                  </button>
                  <button className="text-xl mr-8">
                    <FontAwesomeIcon icon={faComment} className='text-gray-500' />
                  </button>
                  <button className="text-xl mr-8">
                    <FontAwesomeIcon icon={faShare} className='text-gray-500' />
                  </button>
                </div>
              </div>
              <div className="border-b border-gray-200 w-full"></div>
            </>
          );
        })}
      </div>
    </div>
  );
}
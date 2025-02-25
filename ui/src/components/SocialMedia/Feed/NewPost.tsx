import { useState } from "react";
import NeumorphButton from "../../commons/neumorph-button";

export default function NewPost() {
  const [value, setValue] = useState('');

  return (
    <div className="rounded-lg w-full p-4">
      <h2 className="mb-4 text-xl font-bold">Compose new Post</h2>
      <textarea
        placeholder="What's on your mind?"
        value={value}
        onChange={(e) => setValue(e.target.value)}
        className="w-full min-h-[100px] resize-none border-none outline-none"
      />
      <div className="flex justify-end mt-4">
        <NeumorphButton intent="black" size="medium" className="uppercase">
          Create Post
        </NeumorphButton>
      </div>
    </div>
  )
}

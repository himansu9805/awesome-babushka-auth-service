const Divider = ({ text }: { text?: string }) => {
  return (
    <div className="flex items-center w-full my-4">
      <hr className="flex-grow border-t border-gray-300" />
      {text && <span className="mx-4 text-gray-500">{text}</span>}
      <hr className="flex-grow border-t border-gray-300" />
    </div>
  );
};

export default Divider;

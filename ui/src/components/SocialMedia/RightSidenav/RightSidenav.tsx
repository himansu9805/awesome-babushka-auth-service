import { JSX, useEffect, useState } from "react";
import DynamicIsland, { DynamicContainer, DynamicDescription, DynamicIslandProvider, DynamicTitle, SizePresets, useDynamicIslandSize } from "../../commons/dynamic-blob";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faClock, faNewspaper } from "@fortawesome/free-regular-svg-icons";
import { GradientHeading } from "@/components/commons/gradient-heading";
import { faBullseye } from "@fortawesome/free-solid-svg-icons";

const LargeView = () => (
  <div className="h-full w-full flex items-center justify-center">
    <span className="text-white">Large View</span>
  </div>
);

const TallView = () => (
  <div className="h-full w-full flex items-center justify-center">
    <span className="text-white">Tall View</span>
  </div>
);

const TimeView = () => (
  <DynamicContainer className="flex items-center justify-center h-full w-full">
    <div className="w-full flex items-center">
      <DynamicDescription className="ml-4 my-auto text-lg text-white ">
        <FontAwesomeIcon icon={faClock} className="text-white" />
      </DynamicDescription>

      <DynamicDescription className="text-white mx-4 text-sm text-left">
        {new Date().toLocaleTimeString()}
      </DynamicDescription>
    </div>
  </DynamicContainer>
);

const NewsView = () => (
  <DynamicContainer className="flex items-center justify-center h-full w-full">
    <div className="w-full flex items-center">
      <DynamicDescription className="ml-4 my-auto text-lg text-white ">
        <FontAwesomeIcon icon={faNewspaper} className="text-white" />
      </DynamicDescription>

      <DynamicDescription className="text-white mx-4 text-sm   text-left">
        Lorem ipsum dolor sit amet, conse ctetur adipiscing elit.
      </DynamicDescription>
    </div>
  </DynamicContainer>
)

const InfoView = () => (
  <DynamicContainer className="flex items-center justify-center h-full w-full">
    <div className="w-full flex items-center justify-between">
      <DynamicDescription className="ml-4 my-auto text-xl text-white ">
        <FontAwesomeIcon icon={faBullseye} className="text-white" />
      </DynamicDescription>
      <div className="mr-4 flex flex-col items-end justify-center">
        <DynamicDescription className="text-white text-xl">
          Focus Area
        </DynamicDescription>
        <DynamicDescription className="text-white text-xs">
          Updates exclusive for you
        </DynamicDescription>
      </div>
    </div>
  </DynamicContainer>
)


const UserFocus = () => {
  const sizeOrder: SizePresets[] = ["compactLong", "large", "tall"];
  const { state: blobState, setSize } = useDynamicIslandSize();
  const [content, setContent] = useState<JSX.Element>(<InfoView />);
  const [currentIndex, setCurrentIndex] = useState(0);
  const renderers: Partial<Record<SizePresets, () => JSX.Element>> = {
    compactLong: NewsView,
    large: LargeView,
    tall: TallView,
  };
  const cycleBlobStates = () => {
    const nextIndex = (currentIndex + 1) % sizeOrder.length;
    setCurrentIndex(nextIndex);
    setSize(sizeOrder[nextIndex]);
    setContent(
      renderers[sizeOrder[nextIndex]]!()
    )
  };
  useEffect(() => {
    setSize('compactLong');
    // setContent(NewsView());
  }, []);

  return (
    <DynamicIsland id="dynamic-blob" onClick={cycleBlobStates}>
      {content}
    </DynamicIsland>
  );
}

export default function RightSideNav() {

  return (
    <div className="flex flex-col items-start justify-start p-4 bg-white border-l border-gray-200 h-screen w-full">
      <DynamicIslandProvider initialSize="compactLong">
        <UserFocus />
      </DynamicIslandProvider>
    </div >
  );
}
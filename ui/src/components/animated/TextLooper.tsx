import React, { useEffect, useRef, useState } from "react";
import { animate } from "animejs";

/**
 * TextLooper component that animates text fading in and out.
 * @param {Object} props - Component properties.
 * @param {string[]} props.texts - Array of texts to loop through.
 * @param {number} [props.duration=2000] - Animation duration in milliseconds.
 */
// @returns {JSX.Element} The rendered component.
// @example
// <TextLooper texts={["Hello, World!", "Welcome to the animation!"]} duration={3000} />


interface TextLooperProps {
  texts: string[];
  duration?: number;
  className?: string;
  style?: React.CSSProperties;
}
const TextLooper: React.FC<TextLooperProps> = ({ texts, duration = 5000, className, style }) => {
  const textRef = useRef(null);
  const [currentTextIndex, setCurrentTextIndex] = useState(0);
  useEffect(() => {
    if (textRef.current) {
      animate(textRef.current, {
        opacity: [0, 1, 0],
        loop: true,
        alternate: true,
        duration: duration / 2,
        ease: "cubicBezier(0.5, 0, 0.5, 1)",
        onLoop: () => {
          setCurrentTextIndex((currentTextIndex + 1) % texts.length);
        },
      });
    }
  }, [currentTextIndex, duration]);

  return <span ref={textRef} className={className} style={style}>{texts[currentTextIndex]}</span>;
}

export default TextLooper;

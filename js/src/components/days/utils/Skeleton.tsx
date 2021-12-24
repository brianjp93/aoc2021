import React from "react";

export function Skeleton(props: React.PropsWithChildren<{}>) {
  return <div className="container mt-3">{props.children}</div>;
}

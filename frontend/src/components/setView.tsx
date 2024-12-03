import { useEffect } from "react";
import { useMap } from "react-leaflet";

export default function SetView({
  lat,
  lng,
  zoom,
}: {
  lat: number;
  lng: number;
  zoom: number;
}) {
  const map = useMap();

  useEffect(() => {
    map.setView([lat, lng]);

    setTimeout(() => {
      map.setZoom(zoom);
    }, 100);
  }, [lat, lng, zoom]);

  return null;
}

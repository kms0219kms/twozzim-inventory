import { useEffect, useRef, useState } from "react";

import { Icon } from "leaflet";
import { MapContainer, Marker, Popup, TileLayer } from "react-leaflet";
import MarkerClusterGroup from "react-leaflet-markercluster";

import { useQuery } from "@tanstack/react-query";

import { MagnifyingGlassIcon } from "@heroicons/react/20/solid";

import SetView from "@/components/setView";
import { Button } from "@/components/ui/button";
import { Toaster } from "@/components/ui/toaster";
import {
  Card,
  CardTitle,
  CardHeader,
  CardContent,
  CardFooter,
} from "@/components/ui/card";

import { searchFuzzy } from "@/lib/fuzzy";
import { useToast } from "@/hooks/use-toast";

import IResponseBody from "@/types/IResponseBody";
import IStore from "@/types/IStore";

import twozzimLogo from "@/assets/images/twozzim-wmpo.png";

import "leaflet/dist/leaflet.css";
import "react-leaflet-markercluster/dist/styles.min.css";

function App() {
  const { toast } = useToast();

  const [center, setCenter] = useState<[number[], number]>([
    [37.5664056, 126.9778222],
    13,
  ]);

  const { data, isFetching } = useQuery<IResponseBody<IStore[]>>({
    queryKey: ["stores"],
    queryFn: async () => {
      const response = await fetch(
        import.meta.env.VITE_API_HOST + "/v1/store/list"
      );
      return response.json();
    },
    refetchInterval: 10 * 60 * 1000,
  });

  const isLoaded = useRef(false);
  const searchInput = useRef<HTMLInputElement>(null);

  const [searchResult, setSearchResult] = useState<IStore[]>([]);

  useEffect(() => {
    if (!isLoaded.current) {
      isLoaded.current = true;

      toast({
        title: "이용방법 안내",
        description:
          "파란색으로 표시된 매장은 재고가 있으며, 클릭하여 주문할 수 있습니다. 빨간색 매장은 품절인 매장, 검은색 매장은 미참여 매장입니다.",
        className: "bg-blue-500 border-blue-500 text-white",
      });

      navigator.geolocation.getCurrentPosition(
        (position) => {
          console.log(position);
          setCenter([
            [position.coords.latitude, position.coords.longitude],
            13,
          ]);
        },
        (error) => {
          console.error(error);
          setCenter([[37.5664056, 126.9778222], 13]);

          setTimeout(() => {
            toast({
              variant: "destructive",
              title: "위치 정보를 가져오지 못했습니다",
              description:
                "위치 정보를 가져오는 데 실패했습니다. 브라우저 설정을 확인해주세요.",
            });
          }, 8000);
        },
        {
          enableHighAccuracy: true,
        }
      );
    }
  }, []);

  useEffect(() => {
    if (!isFetching && searchResult.length === 0) {
      setSearchResult(data!.data);
    }
  }, [isFetching, searchResult]);

  const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setSearchResult(searchFuzzy(searchInput.current!.value, data!.data));

    console.log(searchFuzzy(searchInput.current!.value, data!.data));
  };

  return (
    <div className="flex font-sans tracking-tight">
      <Toaster />

      <div className="flex flex-col gap-6 w-[450px] h-dvh pt-16 px-10">
        <div
          className="flex flex-col gap-1 cursor-pointer"
          onClick={() => {
            window.location.reload();
          }}
        >
          <img src={twozzimLogo} className="w-28 -ml-2" />

          <h1 className="text-2xl font-semibold tracking-tighter text-neutral-950">
            이세계아이돌 X 두찜 실시간 재고 현황
          </h1>
        </div>

        <form className="relative w-full" onSubmit={handleSubmit}>
          <input
            id="store-search"
            ref={searchInput}
            className="peer w-full border-0 border-b-[1.5px] border-b-neutral-800 bg-transparent pb-2.5 pl-1 pr-10 pt-6 text-lg text-neutral-800 outline-none dark:border-b-neutral-200 dark:text-neutral-100"
            required
          />
          <label
            className="absolute left-1 top-[25.5px] font-sans text-base text-neutral-400 transition-all duration-500 ease-in-out peer-valid:top-0 peer-valid:text-sm peer-valid:text-neutral-800 peer-focus:top-0 peer-focus:text-sm peer-focus:text-neutral-800 dark:peer-valid:text-neutral-200 dark:peer-focus:text-neutral-200"
            htmlFor="store-search"
          >
            지점명이나 지역을 입력해 보세요.
          </label>
          <button type="submit">
            <MagnifyingGlassIcon className="absolute right-1 top-7 size-5 text-neutral-400" />
          </button>
        </form>

        <div className="flex flex-col gap-6 mt-3 mb-8 overflow-scroll h-full">
          {!isFetching &&
            searchResult?.map((store) => (
              <Card
                key={store.id}
                className="cursor-pointer"
                onClick={() => {
                  setCenter([[store.lat, store.lng], 16]);
                }}
              >
                <CardHeader>
                  <CardTitle>{store.name}</CardTitle>
                  {/* <CardDescription>{store.address}</CardDescription> */}
                </CardHeader>
                <CardContent>
                  <p>
                    영업 여부:{" "}
                    {store.operating ? "영업 중" : "영업 종료 (혹은 준비 중)"}
                  </p>
                  <p>
                    품절 여부:{" "}
                    {store.parcipating
                      ? store.is_soldout
                        ? "품절 (혹은 판매 중지)"
                        : "재고 있음"
                      : "미참여 매장"}
                  </p>
                </CardContent>
                {store.parcipating && !store.is_soldout && (
                  <CardFooter>
                    <Button
                      onClick={() => {
                        window.open(
                          "https://twozzim.wmpoplus.com/store/" +
                            store.wmpoplus_id
                        );
                      }}
                    >
                      주문 바로가기
                    </Button>
                  </CardFooter>
                )}
              </Card>
            ))}
        </div>
      </div>

      <MapContainer
        center={[37.5664056, 126.9778222]}
        zoom={13}
        maxBounds={[
          [32, 123],
          [44, 132.5],
        ]}
        className="h-dvh w-[calc(100dvw-450px)]"
      >
        <TileLayer
          attribution='상점 데이터 제공: <a href="https://twozzim.wmpoplus.com">두찜 위메프오</a> | &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          url={`${import.meta.env.VITE_OSM_HOST}/{z}/{x}/{y}.png`}
          maxZoom={19}
        />

        {/* @ts-expect-error - x */}
        <MarkerClusterGroup>
          {!isFetching &&
            data!.data.map((store: any) => (
              <Marker
                key={store.id}
                position={[store.lat, store.lng]}
                title={store.name}
                icon={
                  new Icon.Default({
                    iconUrl: !store.parcipating
                      ? "marker-icon-black.png"
                      : store.is_soldout
                      ? "marker-icon-red.png"
                      : "marker-icon-blue.png",
                    iconRetinaUrl: !store.parcipating
                      ? "marker-icon-2x-black.png"
                      : store.is_soldout
                      ? "marker-icon-2x-red.png"
                      : "marker-icon-2x-blue.png",
                    imagePath:
                      "https://cdn.jsdelivr.net/gh/pointhi/leaflet-color-markers@master/img/",
                    className:
                      !store.parcipating || store.is_soldout
                        ? "!opacity-50"
                        : "",
                  })
                }
              >
                <Popup>
                  <div>
                    <h1>{store.name}</h1>
                    <p>
                      영업 여부:{" "}
                      {store.operating ? "영업 중" : "영업 종료 (혹은 준비 중)"}
                    </p>
                    <p>
                      품절 여부:{" "}
                      {store.parcipating
                        ? store.is_soldout
                          ? "품절 (혹은 판매 중지)"
                          : "재고 있음"
                        : "미참여 매장"}
                    </p>
                    {store.parcipating && !store.is_soldout && (
                      <Button
                        onClick={() => {
                          window.open(
                            "https://twozzim.wmpoplus.com/store/" +
                              store.wmpoplus_id
                          );
                        }}
                      >
                        주문 바로가기
                      </Button>
                    )}
                  </div>
                </Popup>
              </Marker>
            ))}
        </MarkerClusterGroup>

        <SetView lat={center[0][0]} lng={center[0][1]} zoom={center[1]} />
      </MapContainer>
    </div>
  );
}

export default App;

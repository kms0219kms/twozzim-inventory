export default interface IStore {
  // 상점의 API ID
  id: number;

  // 상점 이름
  name: string;

  // 상점이 영업 중인지 여부
  operating: boolean;

  // 상점이 이벤트 참여 매장인지 여부
  parcipating: boolean;

  // 상점 내 재고가 소진되었는지 여부
  is_soldout: boolean;

  // 상점의 위도, 경도
  lat: number;
  lng: number;
}

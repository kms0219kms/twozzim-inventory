import IStore from "@/types/IStore";
import { matches } from "kled";

export function searchFuzzy(
  inputText: string,
  dataArray: IStore[],
  threshold: number = 0.2
): IStore[] {
  const results: { item: IStore; similarity: number }[] = [];

  dataArray.forEach((item) => {
    const nameForSearch = item.name
      .replace(/ /g, "")
      .replace("두마리찜닭두찜", ""); // 공백 제거

    console.log(nameForSearch, matches(inputText, nameForSearch));
    const similarity = matches(inputText, nameForSearch);

    if (similarity >= threshold) {
      results.push({ item, similarity });
    }
  });

  // 유사도 기준으로 내림차순 정렬 (가장 유사한 항목부터)
  results.sort((a, b) => b.similarity - a.similarity);

  return results.map((result) => result.item); // 항목만 반환
}

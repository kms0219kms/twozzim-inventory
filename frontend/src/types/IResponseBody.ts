export default interface IResponseBody<T> {
  code: string;
  status: string;
  data: T;
}

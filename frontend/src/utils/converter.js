import { comparison } from "../mock/docs";

export function renameFile(file, title) {
  const arrExtension = file.name.split(".");
  const extension = arrExtension[arrExtension.length - 1];
  const newFile = new File([file], `${comparison[title]}.${extension}`, {
    type: file.type,
  });
  return newFile;
}

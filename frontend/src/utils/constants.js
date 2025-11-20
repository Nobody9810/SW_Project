// 定义所有板块的元数据
export const CATEGORIES = {
  news: { label: '通讯', apiPath: 'news', hasImage: true },
  books: { label: '书讯', apiPath: 'books', hasImage: true },
  reviews: { label: '书评', apiPath: 'reviews', hasImage: true },
  opinions: { label: '观点', apiPath: 'opinions', hasImage: true },
  literature: { label: '文艺', apiPath: 'literature', hasImage: true },
  history: { label: '文史', apiPath: 'history', hasImage: true },
  library: { label: '书库', apiPath: 'library', hasPdf: true }, // PDF类
  papers: { label: '论文', apiPath: 'papers', hasPdf: true },   // PDF类
  classics: { label: '古籍', apiPath: 'classics', hasPdf: true }, // PDF类
  translations: { label: '译林', apiPath: 'translations', hasImage: true },
  qa: { label: '问答', apiPath: 'qa' },
  scriptures: { label: '经训', apiPath: 'scriptures' },
};

export const NAV_ITEMS = Object.entries(CATEGORIES).map(([key, val]) => ({
  key,
  label: val.label,
  path: `/${key}`
}));
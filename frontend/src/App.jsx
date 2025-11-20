import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import Layout from './components/layout/layout';
import ArticleList from './pages/ArticleList';
import ArticleDetail from './pages/ArticleDetail';

function App() {
  return (
    <Routes>
      <Route path="/" element={<Layout />}>
        {/* 默认重定向到通讯 */}
        <Route index element={<Navigate to="/news" replace />} />
        
        {/* 动态路由匹配所有类别 */}
        <Route path=":category" element={<ArticleList />} />
        <Route path=":category/:id" element={<ArticleDetail />} />
      </Route>
    </Routes>
  );
}

export default App;
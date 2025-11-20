import React from 'react';
import { useParams } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import { Typography, Paper, Box, Divider, Button } from '@mui/material';
import parse from 'html-react-parser'; // 解析 CKEditor 的 HTML
import client from '../api/client';
import { CATEGORIES } from '../utils/constants';
import LikeButton from '../components/interaction/LikeButton';
import Comments from '../components/interaction/Comments';

const ArticleDetail = () => {
  const { category, id } = useParams();
  const config = CATEGORIES[category];

  const { data: article, isLoading } = useQuery({
    queryKey: ['article', category, id],
    queryFn: () => client.get(`articles/${config.apiPath}/${id}/`)
  });

  if (isLoading) return <div>加载内容中...</div>;
  if (!article) return <div>文章未找到</div>;

  // PDF 渲染逻辑
  const renderContent = () => {
    if (config.hasPdf && article.document_url) {
      return (
        <Box sx={{ height: '800px', mt: 2 }}>
           {/* 使用 iframe 预览 PDF，简单且兼容性好。也可以换成 react-pdf */}
          <iframe 
            src={article.document_url} 
            width="100%" 
            height="100%" 
            style={{ border: 'none' }}
            title="PDF Viewer"
          />
          <Button variant="contained" href={article.document_url} download sx={{ mt: 2 }}>
            下载 PDF
          </Button>
        </Box>
      );
    }
    
    // 普通富文本渲染
    return (
      <Box sx={{ mt: 2, '& img': { maxWidth: '100%', height: 'auto' } }}>
        {article.content ? parse(article.content) : <Typography>暂无文字内容</Typography>}
      </Box>
    );
  };

  return (
    <Paper elevation={3} sx={{ p: 4 }}>
      {/* 标题区 */}
      <Typography variant="h3" gutterBottom>{article.title}</Typography>
      
      <Box sx={{ display: 'flex', gap: 2, color: 'text.secondary', mb: 3, alignItems: 'center' }}>
        <Typography>作者: {article.author || article.original_author || '未知'}</Typography>
        <Divider orientation="vertical" flexItem />
        <Typography>发布: {article.created_at}</Typography>
        <Divider orientation="vertical" flexItem />
        <Typography>浏览: {article.total_views}</Typography>
        
        {/* 点赞组件 */}
        <Box sx={{ ml: 'auto' }}>
          <LikeButton 
            model={article.type} // 从后端 Serializer 获取的 type 字段
            id={article.id} 
            likes={article.likes} 
            dislikes={article.dislikes} 
          />
        </Box>
      </Box>

      <Divider />

      {/* 内容区 (文本 或 PDF) */}
      {renderContent()}

      <Divider sx={{ my: 4 }} />

      {/* 评论区 */}
      <Comments model={article.type} objectId={article.id} />
    </Paper>
  );
};

export default ArticleDetail;
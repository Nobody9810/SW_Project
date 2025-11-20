import React from 'react';
import { useParams } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import { Grid, Card, CardContent, CardMedia, Typography, CardActionArea, Chip, Stack } from '@mui/material';
import { useNavigate } from 'react-router-dom';
import client from '../api/client';
import { CATEGORIES } from '../utils/constants';

const ArticleList = () => {
  const { category } = useParams(); // 获取 URL 中的 category (如 'news')
  const navigate = useNavigate();
  const config = CATEGORIES[category];

  // 数据获取
  const { data, isLoading, error } = useQuery({
    queryKey: ['articles', category],
    queryFn: () => client.get(`articles/${config.apiPath}/`)
  });

  if (!config) return <div>板块不存在</div>;
  if (isLoading) return <div>加载中...</div>;
  if (error) return <div>加载失败</div>;

  return (
    <div>
      <Typography variant="h4" gutterBottom sx={{ mb: 4, borderLeft: '5px solid #1976d2', pl: 2 }}>
        {config.label}
      </Typography>

      <Grid container spacing={3}>
        {data.results.map((item) => (
          <Grid item xs={12} sm={6} md={4} key={item.id}>
            <Card sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
              <CardActionArea onClick={() => navigate(`/${category}/${item.id}`)}>
                {/* 如果有图片且不是null，显示图片；否则显示占位 */}
                {(config.hasImage || item.image) && (
                  <CardMedia
                    component="img"
                    height="140"
                    image={item.image || "https://via.placeholder.com/300x140?text=No+Image"}
                    alt={item.title}
                  />
                )}
                <CardContent>
                  <Typography gutterBottom variant="h6" component="div" noWrap>
                    {item.title}
                  </Typography>
                  <Stack direction="row" spacing={1} mb={1}>
                    <Chip label={`浏览: ${item.total_views}`} size="small" variant="outlined" />
                    <Chip label={item.created_at.split('T')[0]} size="small" />
                  </Stack>
                  <Typography variant="body2" color="text.secondary" sx={{
                    display: '-webkit-box',
                    overflow: 'hidden',
                    WebkitBoxOrient: 'vertical',
                    WebkitLineClamp: 3,
                  }}>
                    {/* 去除HTML标签简单的预览 */}
                    {item.content ? item.content.replace(/<[^>]+>/g, '') : (item.author_intro || '点击查看详情')}
                  </Typography>
                </CardContent>
              </CardActionArea>
            </Card>
          </Grid>
        ))}
      </Grid>
    </div>
  );
};

export default ArticleList;
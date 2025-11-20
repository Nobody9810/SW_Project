import React from 'react';
import { IconButton, Badge, Stack, Tooltip } from '@mui/material';
import { ThumbUp, ThumbDown, ThumbUpOutlined, ThumbDownOutlined } from '@mui/icons-material';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import client from '../../api/client';

const LikeButton = ({ model, id, likes, dislikes }) => {
  const queryClient = useQueryClient();

  // 记录本地点击状态 (为了UI即时反馈，也可以存localStorage)
  const [userAction, setUserAction] = React.useState(null); 

  const mutation = useMutation({
    mutationFn: (type) => client.post('reactions/toggle/', { model, id, type }),
    onSuccess: (data) => {
      // 更新 UI 状态
      if (data.action === 'created' || data.action === 'switched') {
        setUserAction(data.current);
      } else {
        setUserAction(null);
      }
      // 使得列表页或详情页的数据失效，触发重新拉取最新计数
      queryClient.invalidateQueries({ queryKey: ['article', model, id] });
    }
  });

  return (
    <Stack direction="row" spacing={2}>
      <Tooltip title="点赞">
        <IconButton onClick={() => mutation.mutate('like')} color={userAction === 'like' ? "primary" : "default"}>
          <Badge badgeContent={likes} color="primary">
            {userAction === 'like' ? <ThumbUp /> : <ThumbUpOutlined />}
          </Badge>
        </IconButton>
      </Tooltip>

      <Tooltip title="点踩">
        <IconButton onClick={() => mutation.mutate('dislike')} color={userAction === 'dislike' ? "error" : "default"}>
          <Badge badgeContent={dislikes} color="error">
            {userAction === 'dislike' ? <ThumbDown /> : <ThumbDownOutlined />}
          </Badge>
        </IconButton>
      </Tooltip>
    </Stack>
  );
};

export default LikeButton;
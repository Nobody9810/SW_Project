import React, { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { Box, TextField, Button, Typography, List, ListItem, Avatar, Divider, Paper } from '@mui/material';
import client from '../../api/client';

// 单条评论组件
const CommentItem = ({ comment, onReply }) => (
  <Box sx={{ mb: 2 }}>
    <Paper elevation={0} sx={{ p: 2, bgcolor: '#f5f5f5' }}>
      <Typography variant="subtitle2" color="primary" sx={{ fontWeight: 'bold' }}>
        {comment.nickname}
      </Typography>
      <Typography variant="body2" sx={{ my: 1 }}>
        {comment.content}
      </Typography>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <Typography variant="caption" color="text.secondary">{comment.created_at}</Typography>
        <Button size="small" onClick={() => onReply(comment.id, comment.nickname)}>回复</Button>
      </Box>
    </Paper>
    
    {/* 递归渲染子评论 */}
    {comment.replies && comment.replies.length > 0 && (
      <Box sx={{ pl: 4, mt: 1, borderLeft: '2px solid #e0e0e0' }}>
        {comment.replies.map(reply => (
          <CommentItem key={reply.id} comment={reply} onReply={onReply} />
        ))}
      </Box>
    )}
  </Box>
);

const Comments = ({ model, objectId }) => {
  const queryClient = useQueryClient();
  const [content, setContent] = useState('');
  const [replyTo, setReplyTo] = useState(null); // { id: 1, name: 'xxx' }

  // 获取评论列表
  const { data: comments = [] } = useQuery({
    queryKey: ['comments', model, objectId],
    queryFn: () => client.get(`comments/?model=${model}&id=${objectId}`)
  });

  // 提交评论
  const mutation = useMutation({
    mutationFn: (newComment) => client.post('comments/', newComment),
    onSuccess: () => {
      setContent('');
      setReplyTo(null);
      queryClient.invalidateQueries(['comments', model, objectId]);
    }
  });

  const handleSubmit = () => {
    if (!content.trim()) return;
    mutation.mutate({
      model,
      object_id: objectId,
      content,
      parent: replyTo?.id || null
    });
  };

  return (
    <Box sx={{ mt: 4 }}>
      <Typography variant="h6" gutterBottom>评论区</Typography>
      
      {/* 输入框 */}
      <Box sx={{ mb: 4 }}>
        {replyTo && (
          <Typography variant="caption" display="block" sx={{ mb: 1 }}>
            正在回复: {replyTo.name} 
            <Button size="small" onClick={() => setReplyTo(null)}>(取消)</Button>
          </Typography>
        )}
        <TextField
          fullWidth
          multiline
          rows={3}
          variant="outlined"
          placeholder={replyTo ? `回复 ${replyTo.name}...` : "写下你的评论..."}
          value={content}
          onChange={(e) => setContent(e.target.value)}
        />
        <Button 
          variant="contained" 
          sx={{ mt: 1 }} 
          onClick={handleSubmit}
          disabled={mutation.isPending}
        >
          {mutation.isPending ? '发送中...' : '发表评论'}
        </Button>
      </Box>

      {/* 列表 */}
      <List>
        {comments.map(comment => (
          <CommentItem 
            key={comment.id} 
            comment={comment} 
            onReply={(id, name) => setReplyTo({ id, name })} 
          />
        ))}
        {comments.length === 0 && <Typography color="text.secondary">暂无评论，快来抢沙发吧！</Typography>}
      </List>
    </Box>
  );
};

export default Comments;
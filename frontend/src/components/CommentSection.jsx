import React, { useState, useEffect } from 'react';
import { MessageSquare, User, Send, Loader2 } from 'lucide-react';
import api from '../api/axios'; // 导入上面配置的 axios

/**
 * 通用评论组件
 * @param {string} modelName - 后端对应的模型名称 (如 'news', 'bookinfo')
 * @param {number} objectId - 文章/对象的 ID
 */
const CommentSection = ({ modelName, objectId }) => {
    const [comments, setComments] = useState([]);
    const [loading, setLoading] = useState(true);
    const [submitting, setSubmitting] = useState(false);
    
    // 表单状态
    const [content, setContent] = useState('');
    const [nickname, setNickname] = useState('');
    const [error, setError] = useState(null);

    // 1. 加载评论
    useEffect(() => {
        const fetchComments = async () => {
            try {
                setLoading(true);
                // 调用后端: GET /api/comments/?model=news&id=1
                const response = await api.get(`/comments/?model=${modelName}&id=${objectId}`);
                setComments(response.data);
            } catch (err) {
                console.error("获取评论失败", err);
                setError("无法加载评论，请稍后再试。");
            } finally {
                setLoading(false);
            }
        };

        if (modelName && objectId) {
            fetchComments();
        }
    }, [modelName, objectId]);

    // 2. 提交评论
    const handleSubmit = async (e) => {
        e.preventDefault();
        if (!content.trim()) return;

        try {
            setSubmitting(true);
            setError(null);

            const payload = {
                model: modelName,
                id: objectId,
                content: content,
                // 如果用户未填昵称，使用默认值
                nickname: nickname.trim() || '匿名书友' 
            };

            // 调用后端: POST /api/comments/
            const response = await api.post('/comments/', payload);

            // 成功后：将新评论添加到列表顶部，并清空输入框
            setComments([response.data, ...comments]);
            setContent('');
            // 可选：保留昵称以便下次评论，或清空
        } catch (err) {
            console.error("提交评论失败", err);
            setError("提交失败，请检查网络或稍后再试。");
        } finally {
            setSubmitting(false);
        }
    };

    // 日期格式化工具
    const formatDate = (dateString) => {
        const date = new Date(dateString);
        return date.toLocaleDateString('zh-CN', {
            year: 'numeric',
            month: 'long',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        });
    };

    return (
        <div className="mt-12 bg-white rounded-xl shadow-sm border border-gray-100 p-6">
            {/* 标题区域 */}
            <div className="flex items-center gap-2 mb-6 border-b border-gray-100 pb-4">
                <MessageSquare className="w-5 h-5 text-blue-600" />
                <h3 className="text-lg font-bold text-gray-800">
                    评论 ({comments.length})
                </h3>
            </div>

            {/* 错误提示 */}
            {error && (
                <div className="mb-4 p-3 bg-red-50 text-red-600 text-sm rounded-lg">
                    {error}
                </div>
            )}

            {/* 评论输入表单 */}
            <form onSubmit={handleSubmit} className="mb-10">
                <div className="flex gap-4">
                    <div className="hidden md:block">
                        <div className="w-10 h-10 rounded-full bg-gray-100 flex items-center justify-center text-gray-400">
                            <User size={20} />
                        </div>
                    </div>
                    <div className="flex-1">
                        <div className="mb-3">
                            <input
                                type="text"
                                placeholder="您的昵称 (可选)"
                                value={nickname}
                                onChange={(e) => setNickname(e.target.value)}
                                className="w-full md:w-1/3 px-3 py-2 bg-gray-50 border border-gray-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 transition-colors"
                            />
                        </div>
                        <div className="relative">
                            <textarea
                                value={content}
                                onChange={(e) => setContent(e.target.value)}
                                placeholder="分享您的观点..."
                                rows="3"
                                className="w-full p-3 bg-gray-50 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 transition-colors resize-none"
                                required
                            />
                            <button
                                type="submit"
                                disabled={submitting || !content.trim()}
                                className="absolute bottom-3 right-3 px-4 py-1.5 bg-blue-600 text-white text-sm font-medium rounded-md hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2 transition-colors shadow-sm"
                            >
                                {submitting ? (
                                    <>
                                        <Loader2 className="w-3 h-3 animate-spin" />
                                        发送中
                                    </>
                                ) : (
                                    <>
                                        发送 <Send className="w-3 h-3" />
                                    </>
                                )}
                            </button>
                        </div>
                    </div>
                </div>
            </form>

            {/* 评论列表 */}
            <div className="space-y-6">
                {loading ? (
                    <div className="flex justify-center py-8 text-gray-400">
                        <Loader2 className="w-6 h-6 animate-spin" />
                    </div>
                ) : comments.length > 0 ? (
                    comments.map((comment) => (
                        <div key={comment.id} className="flex gap-4 animate-in fade-in slide-in-from-bottom-2 duration-500">
                            <div className="flex-shrink-0">
                                <div className="w-10 h-10 rounded-full bg-indigo-50 text-indigo-500 flex items-center justify-center font-bold text-sm">
                                    {comment.nickname.charAt(0).toUpperCase()}
                                </div>
                            </div>
                            <div className="flex-1">
                                <div className="flex items-center justify-between mb-1">
                                    <span className="font-semibold text-gray-800">
                                        {comment.nickname}
                                    </span>
                                    <span className="text-xs text-gray-400">
                                        {formatDate(comment.created_at)}
                                    </span>
                                </div>
                                <p className="text-gray-600 text-sm leading-relaxed whitespace-pre-wrap">
                                    {comment.content}
                                </p>
                            </div>
                        </div>
                    ))
                ) : (
                    <div className="text-center py-10 bg-gray-50 rounded-lg border border-dashed border-gray-200">
                        <p className="text-gray-500 text-sm">暂无评论，快来抢占沙发吧！</p>
                    </div>
                )}
            </div>
        </div>
    );
};

export default CommentSection;
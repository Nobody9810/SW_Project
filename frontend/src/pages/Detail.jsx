import { useParams } from 'react-router-dom';
import CommentSection from '../components/CommentSection';
// ... 其他导入

const NewsDetail = () => {
    const { id } = useParams();
    // ... 获取文章详情的逻辑

    return (
        <div className="max-w-4xl mx-auto p-4">
            {/* ... 文章内容 ... */}
            
            <hr className="my-8 border-gray-200" />
            
            {/* 插入评论区 */}
            {/* modelName 必须是后端 ContentType 能识别的小写模型名 */}
            <CommentSection modelName="news" objectId={id} />
        </div>
    );
};

export default NewsDetail;
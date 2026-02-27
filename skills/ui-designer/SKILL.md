---
name: ui-designer
description: |
  专业的 UI/UX 设计助手，帮助快速创建、优化和转换界面设计。
  
  功能包括：
  1. 根据描述生成 React/Tailwind 组件代码
  2. 优化现有 UI 的样式和布局
  3. 生成响应式设计方案
  4. 创建设计系统（颜色、字体、间距）
  5. 将设计稿转换为代码（HTML/React/Vue）
  6. 生成图标和图形资源
  
  触发场景：
  - 用户需要创建新的 UI 组件或页面
  - 用户想要优化现有界面的设计
  - 用户需要将设计稿转换为代码
  - 用户需要生成设计系统或样式指南
  - 用户需要创建响应式布局
  - 用户需要设计移动端或桌面端界面
---

# UI Designer - 专业界面设计助手

## 核心能力

### 1. 组件生成
根据自然语言描述生成可直接使用的 UI 组件代码。

**支持框架**：
- React + Tailwind CSS（推荐）
- Vue 3 + Tailwind CSS
- 纯 HTML + CSS

**组件类型**：
- 按钮、输入框、表单元素
- 卡片、列表、表格
- 导航栏、侧边栏、标签页
- 弹窗、抽屉、下拉菜单
- 图表、数据可视化

### 2. 设计优化
分析和优化现有 UI 代码，提升视觉效果和用户体验。

**优化维度**：
- 颜色对比度和可访问性
- 间距和布局一致性
- 字体层次和可读性
- 交互反馈和动效
- 响应式适配

### 3. 设计系统生成
创建完整的设计系统，确保项目视觉一致性。

**输出内容**：
- 颜色调色板（主色、辅助色、中性色）
- 字体规范（标题、正文、辅助文字）
- 间距系统（4px 基准网格）
- 圆角和阴影规范
- 组件设计规范

### 4. 响应式设计
为不同屏幕尺寸生成适配方案。

**断点标准**：
- 移动端：< 640px
- 平板：640px - 1024px
- 桌面：> 1024px

## 使用指南

### 生成组件

用户："帮我创建一个登录表单，要有邮箱、密码输入框和登录按钮"

思考过程：
1. 确定使用 React + Tailwind
2. 包含邮箱输入、密码输入、登录按钮
3. 添加基本的表单验证样式
4. 确保移动端友好

输出：
```tsx
export function LoginForm() {
  return (
    <form className="space-y-4 w-full max-w-md mx-auto p-6 bg-white rounded-xl shadow-lg">
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-1">邮箱</label>
        <input
          type="email"
          className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          placeholder="your@email.com"
        />
      </div>
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-1">密码</label>
        <input
          type="password"
          className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          placeholder="••••••••"
        />
      </div>
      <button
        type="submit"
        className="w-full py-2 px-4 bg-blue-600 hover:bg-blue-700 text-white font-medium rounded-lg transition-colors"
      >
        登录
      </button>
    </form>
  );
}
```

### 优化现有 UI

用户："优化这个按钮的样式，让它更现代"

原始代码：
```tsx
<button className="btn">点击</button>
```

优化后：
```tsx
<button className="px-6 py-2.5 bg-gradient-to-r from-blue-600 to-blue-700 hover:from-blue-700 hover:to-blue-800 text-white font-medium rounded-lg shadow-md hover:shadow-lg transform hover:-translate-y-0.5 transition-all duration-200 active:scale-95">
  点击
</button>
```

### 生成设计系统

用户："为我的足球 App 创建一个设计系统，主色是蓝色"

输出：
```typescript
// design-system.ts
export const colors = {
  primary: {
    50: '#eff6ff',
    100: '#dbeafe',
    500: '#3b82f6',
    600: '#2563eb',
    700: '#1d4ed8',
    900: '#1e3a8a',
  },
  // ... 其他颜色
};

export const typography = {
  h1: 'text-3xl font-bold tracking-tight',
  h2: 'text-2xl font-semibold tracking-tight',
  body: 'text-base leading-relaxed',
  caption: 'text-sm text-gray-600',
};

export const spacing = {
  xs: '4px',
  sm: '8px',
  md: '16px',
  lg: '24px',
  xl: '32px',
};
```

## 设计原则

### 1. 简洁优先
- 使用最少的元素传达信息
- 避免过度装饰
- 保持界面清爽

### 2. 一致性
- 统一的颜色系统
- 一致的间距和排版
- 标准化的组件样式

### 3. 可访问性
- 确保足够的颜色对比度（WCAG AA 标准）
- 支持键盘导航
- 提供清晰的视觉反馈

### 4. 响应式
- 移动优先设计
- 流式布局
- 适配各种屏幕尺寸

## 最佳实践

### 颜色使用
- 主色用于主要操作和品牌元素
- 辅助色用于区分不同状态
- 中性色用于背景和文字
- 避免使用超过 3 种主色

### 排版规范
- 标题使用无衬线字体（如 Inter、SF Pro）
- 正文行高 1.5-1.7
- 标题字重 600-700，正文字重 400
- 使用字体大小建立视觉层次

### 间距系统
- 基于 4px 或 8px 的网格系统
- 相关元素间距 8-16px
- 区块间距 24-32px
- 保持一致的间距节奏

### 圆角和阴影
- 小元素圆角 4-6px
- 卡片圆角 8-12px
- 使用柔和的阴影（透明度 5-15%）
- 避免过重的阴影效果

## 输出格式

### React + Tailwind（默认）
```tsx
export function ComponentName() {
  return (
    // JSX code
  );
}
```

### Vue 3
```vue
<template>
  // Template code
</template>

<script setup>
// Script code
</script>
```

### 纯 HTML
```html
<div class="...">
  <!-- HTML code -->
</div>
```

## 示例

### 示例 1：新闻卡片
输入："创建一个新闻卡片组件，有图片、标题、摘要和发布时间"

输出：
```tsx
interface NewsCardProps {
  image: string;
  title: string;
  summary: string;
  publishedAt: string;
}

export function NewsCard({ image, title, summary, publishedAt }: NewsCardProps) {
  return (
    <div className="bg-white rounded-xl shadow-md overflow-hidden hover:shadow-lg transition-shadow">
      <img src={image} alt={title} className="w-full h-48 object-cover" />
      <div className="p-4">
        <h3 className="text-lg font-semibold text-gray-900 mb-2 line-clamp-2">{title}</h3>
        <p className="text-gray-600 text-sm mb-3 line-clamp-2">{summary}</p>
        <time className="text-xs text-gray-400">{publishedAt}</time>
      </div>
    </div>
  );
}
```

### 示例 2：导航栏
输入："创建一个响应式导航栏，有 Logo、导航链接和用户头像"

输出：
```tsx
export function Navbar() {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <nav className="bg-white shadow-sm">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          {/* Logo */}
          <div className="flex items-center">
            <span className="text-xl font-bold text-blue-600">Logo</span>
          </div>

          {/* Desktop Navigation */}
          <div className="hidden md:flex items-center space-x-8">
            <a href="#" className="text-gray-700 hover:text-blue-600 transition-colors">首页</a>
            <a href="#" className="text-gray-700 hover:text-blue-600 transition-colors">新闻</a>
            <a href="#" className="text-gray-700 hover:text-blue-600 transition-colors">比赛</a>
          </div>

          {/* User Avatar */}
          <div className="flex items-center">
            <img
              src="/avatar.jpg"
              alt="User"
              className="h-8 w-8 rounded-full border-2 border-gray-200"
            />
          </div>

          {/* Mobile Menu Button */}
          <button
            className="md:hidden p-2"
            onClick={() => setIsOpen(!isOpen)}
          >
            <Menu className="h-6 w-6" />
          </button>
        </div>
      </div>

      {/* Mobile Menu */}
      {isOpen && (
        <div className="md:hidden">
          <div className="px-2 pt-2 pb-3 space-y-1">
            <a href="#" className="block px-3 py-2 rounded-md text-base font-medium text-gray-700 hover:text-blue-600 hover:bg-gray-50">首页</a>
            <a href="#" className="block px-3 py-2 rounded-md text-base font-medium text-gray-700 hover:text-blue-600 hover:bg-gray-50">新闻</a>
            <a href="#" className="block px-3 py-2 rounded-md text-base font-medium text-gray-700 hover:text-blue-600 hover:bg-gray-50">比赛</a>
          </div>
        </div>
      )}
    </nav>
  );
}
```

## 注意事项

1. **代码质量**：生成的代码应该是生产就绪的，包含适当的 TypeScript 类型
2. **可维护性**：使用清晰的命名和结构，方便后续修改
3. **性能**：避免不必要的重渲染，使用适当的 React 优化技巧
4. **兼容性**：确保代码在现代浏览器中正常运行
5. **国际化**：考虑多语言支持，避免硬编码中文样式

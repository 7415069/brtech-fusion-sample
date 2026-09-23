// src/api/sample/index.ts
/**
 * brtech 底座 - API 调用示例
 *
 * 演示如何使用 brtech-fusion 的 request 工具调用后端自动生成的 CRUD 接口。
 * 所有接口遵循统一模式：
 *
 *   POST /{module}/add           - 新增
 *   POST /{module}/delete        - 删除
 *   POST /{module}/update        - 更新
 *   POST /{module}/find/{id}     - 按 ID 查询
 *   POST /{module}/find/batch    - 批量查询
 *   POST /{module}/query/page    - 分页查询
 *   POST /{module}/query/all     - 查询全部
 *   POST /{module}/excel/import  - Excel 导入
 *   POST /{module}/excel/export  - Excel 导出
 */
import {request, type Response} from 'brtech-fusion'

// ============================================================
// 类型定义 — 字段名与后端 models.py 保持一致
// ============================================================

export interface SampleNormal {
  modelId: string
  stringField: string
  lobStringField?: string
  intField?: number
  selectField: string
  selectFieldDisplay?: string
  switchField: string
  switchFieldDisplay?: string
  dateField?: string
  imageField?: string
  treeselectField?: string
  jsonField?: any[]
  colorField?: string
  tagField?: string[]
  createTimestamp?: string
  updateTimestamp?: string
}

export interface SampleRecurse {
  modelId: string
  label: string
  code: string
  sortOrder: number
  parentId?: string
  children?: SampleRecurse[]
}

// ============================================================
// 普通模型 API 示例
// ============================================================

export const NormalApi = {
  async add(data: Partial<SampleNormal>) {
    const {data: res} = await request.post<Response<SampleNormal>>('/normal/add', data)
    return res
  },
  async delete(modelId: string) {
    const {data: res} = await request.post<Response<void>>('/normal/delete', {modelId})
    return res
  },
  async update(data: Partial<SampleNormal>) {
    const {data: res} = await request.post<Response<SampleNormal>>('/normal/update', data)
    return res
  },
  async findById(modelId: string) {
    const {data: res} = await request.post<Response<SampleNormal>>(`/normal/find/${modelId}`)
    return res?.data
  },
  async queryPage(params: Record<string, any>) {
    const {data: res} = await request.post<Response<{
      content: SampleNormal[]
      total: number
      page: number
      size: number
    }>>('/normal/query/page', params)
    return res
  },
  async queryAll(params?: Record<string, any>) {
    const {data: res} = await request.post<Response<SampleNormal[]>>('/normal/query/all', params || {})
    return res?.data || []
  },
  async customAction(modelId: string) {
    const {data: res} = await request.post<Response<string>>(`/normal/customAction/${modelId}`)
    return res?.data
  },
}

// ============================================================
// 递归模型 API 示例 (树形结构)
// ============================================================

export const RecurseApi = {
  async add(data: Partial<SampleRecurse>) {
    const {data: res} = await request.post<Response<SampleRecurse>>('/recurse/add', data)
    return res
  },
  async delete(modelId: string) {
    const {data: res} = await request.post<Response<void>>('/recurse/delete', {modelId})
    return res
  },
  async update(data: Partial<SampleRecurse>) {
    const {data: res} = await request.post<Response<SampleRecurse>>('/recurse/update', data)
    return res
  },
  async queryPage(params: Record<string, any>) {
    const {data: res} = await request.post<Response<{
      content: SampleRecurse[]
      total: number
    }>>('/recurse/query/page', params)
    return res
  },
  async queryAll(params?: Record<string, any>) {
    const {data: res} = await request.post<Response<SampleRecurse[]>>('/recurse/query/all', params || {})
    return res?.data || []
  },
}
